# Attention

The celebrated attention formula `softmax(Q K^T)` is easy to interpret
for a single query q; matrix Q is vectorizing that case across all
queries at once. A query asks: of a sample that landed on the
best-matching key, how likely is it to have come from each key?
Normalized, that's the attention weights. Each key's score is `q ·
k_i`, the projection of `k_i` onto `q` and it is a single number of a
line. From the query's view there is no high-dimensional space, just
scores `s_i = q · k_i`.

Slide the line so the max sits at `0`; every other key is a gap below it,
`gap_i = max(s) - s_i`. Read each gap as a squared distance,

```
dist_i = sqrt( max(s) - s_i )
```

so the best key sits at `0` and the rest scatter out to the right. Now
put a Gaussian at each site, width `w = 1/√|q|`. Assume a sample landed at
0. Which site produced it? Read each Gaussian at the sample:

```
L_i ~ exp( -dist_i² / w² )      P_i = L_i / Σ_j L_j
```

![Attention](attention.png)

Each key is a Gaussian centered on its site; the vertical line is the
sample. It was most likely produced by the best-matching site, but
could also have come from another.


For example,

```python
import numpy as np
w = 3/2                              # |q|
k = np.array([-10, -5, -2, -1, 1])   # scores q · k
gap  = k.max() - k
dist = np.sqrt(gap)
L    = np.exp(-dist**2 / w**2)
P    = L / L.sum()
print(*(f"{100*x:02.0f}" for x in P))     # 00 04 15 23 57
```

And the whole thing, with the softmax written as the likelihood, and
it matches PyTorch's MultiheadAttention. So batch, heads, and
queries dimensions are just independent copies of the same one-query likelihood,
vectorized:

```python
import torch, torch.nn as nn, einx


class MultiHeadCrossAttention(nn.Module):

    def __init__(self, embed_dim, num_heads):
        super().__init__()
        self.h = num_heads
        d_head, q = divmod(embed_dim, num_heads)
        assert q == 0, "embed_dim must be divisible by num_heads"
        self.q_proj = nn.Linear(embed_dim, embed_dim)
        self.k_proj = nn.Linear(embed_dim, embed_dim)
        self.v_proj = nn.Linear(embed_dim, embed_dim)
        self.o_proj = nn.Linear(embed_dim, embed_dim)
        self.scale = 1 / d_head**0.5

    def forward(self, x_q, x_kv):
        q = self.q_proj(x_q)
        k = self.k_proj(x_kv)
        v = self.v_proj(x_kv)
        scores = einx.dot("i b (h d), j b (h d) -> b h i j", q, k,
                          h=self.h) * self.scale
        msc = scores.amax(dim=-1, keepdim=True)
        gap = msc - scores
        dist = gap.sqrt()
        L = torch.exp(-dist**2)
        attn = L / einx.sum("b h i ([j])", L)
        out = einx.dot("b h i j, j b (h d) -> i b (h d)", attn, v, h=self.h)
        return self.o_proj(out)


embed_dim = 15
num_heads = 5
B, S_q, S_kv = 2, 4, 6
a = torch.nn.MultiheadAttention(embed_dim=embed_dim, num_heads=num_heads)
b = MultiHeadCrossAttention(embed_dim=embed_dim, num_heads=num_heads)
with torch.no_grad():
    a.in_proj_weight.copy_(
        einx.rearrange("q d, k d, v d -> (q + k + v) d", b.q_proj.weight,
                       b.k_proj.weight, b.v_proj.weight))
    a.in_proj_bias.copy_(
        einx.rearrange("q, k, v -> (q + k + v)", b.q_proj.bias, b.k_proj.bias,
                       b.v_proj.bias))
    a.out_proj.weight.copy_(b.o_proj.weight)
    a.out_proj.bias.copy_(b.o_proj.bias)

x_q = torch.randn(S_q, B, embed_dim)
x_kv = torch.randn(S_kv, B, embed_dim)
a_out, _ = a(x_q, x_kv, x_kv)
b_out = b(x_q, x_kv)

print(torch.allclose(a_out, b_out, atol=1e-6))
```
