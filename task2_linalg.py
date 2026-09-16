"""
ELEC 576 / COMP 576 - Assignment 0, Task 2
Run every Python command in the "Linear Algebra Equivalents" table of
"NumPy for MATLAB Users" (https://numpy.org/doc/stable/user/numpy-for-matlab-users.html)
inside IPython and record the transcript.

Run with:  ipython task2_linalg.py
"""
import re
import textwrap
from IPython.core.interactiveshell import InteractiveShell
from IPython.utils.capture import capture_output

shell = InteractiveShell.instance()
shell.colors = "NoColor"

_n = 0


def run(cmd, seen=None):
    """Execute one line in the IPython shell and echo it as an In/Out pair.

    Within a row, a spelling that reproduces an earlier spelling's output exactly
    is reported as such instead of reprinting the whole array.
    """
    global _n
    cmd = re.sub(r"\s+#.*$", "", cmd)
    _n += 1
    print(f"In [{_n}]: {cmd}")
    with capture_output() as cap:
        res = shell.run_cell(cmd, store_history=False)
    body = cap.stdout.rstrip("\n")
    if res.result is not None and not body:
        body = repr(res.result)
    body = re.sub(r"^Out\[\d+\]:", f"Out[{_n}]:", body, flags=re.M)
    if body and seen is not None and body.count("\n") >= 2:
        key = re.sub(r"^Out\[\d+\]:", "", body, flags=re.M)
        if key in seen:
            print(f"Out[{_n}]: identical to Out[{seen[key]}]")
            body = ""
        else:
            seen[key] = _n
    if body:
        print(body)
    if res.error_in_exec is not None:
        print(f"         {type(res.error_in_exec).__name__}: {res.error_in_exec}")


def row(num, matlab, cmds, note=None):
    hdr = f"--- Row {num} --- MATLAB: {matlab} "
    print("\n" + hdr + "-" * max(3, 78 - len(hdr)))
    seen = {}
    for c in cmds:
        run(c, seen)


# ---------------------------------------------------------------- setup ----
SETUP = [
    "import numpy as np",
    "import scipy.linalg",
    "from numpy.random import default_rng",
    "from scipy import signal",
    "from scipy.sparse.linalg import eigs, cg",
    "linalg = scipy.linalg          # the assignment asks us to import scipy.linalg",
    "np.set_printoptions(precision=4, suppress=True, linewidth=100)",
    "seed = default_rng(576)",
    "a = np.round(seed.random((5, 5)), 2)",
    "b = np.round(seed.random((5, 5)), 2)",
    "c = np.round(seed.random((5, 5)), 2)",
    "d = np.round(seed.random((5, 5)), 2)",
    "v = np.round(seed.random(5), 2)",
    "x = a.copy()",
    "m, n, q = 2, 2, 2",
    "ai = seed.integers(0, 8, (5, 5))          # integer arrays, for the bitwise rows",
    "bi = seed.integers(0, 8, (5, 5))",
    "spd = a @ a.T + 5 * np.eye(5)             # symmetric positive definite, for chol / cg",
    "sig = np.round(seed.random(12), 2)        # a 1-D signal, for resample",
    "a_orig = a.copy()                         # kept so the in-place rows can be undone",
    "a",
    "b",
    "v",
]

print("--- Setup " + "-" * 68)
for s in SETUP:
    run(s)

# ------------------------------------------------------------- the table ----
row(1, "ndims(a)", ["np.ndim(a)", "a.ndim"])
row(2, "numel(a)", ["np.size(a)", "a.size"])
row(3, "size(a)", ["np.shape(a)", "a.shape"])
row(4, "size(a,n)", ["a.shape[n-1]"])
row(5, "[ 1 2 3; 4 5 6 ]", ["np.array([[1., 2., 3.], [4., 5., 6.]])"])
row(6, "[ a b; c d ]", ["np.block([[a, b], [c, d]])"])
row(7, "a(end)", ["a[-1]"])
row(8, "a(2,5)", ["a[1, 4]"])
row(9, "a(2,:)", ["a[1]", "a[1, :]"])
row(10, "a(1:5,:)", ["a[0:5]", "a[:5]", "a[0:5, :]"])
row(11, "a(end-4:end,:)", ["a[-5:]"])
row(12, "a(1:3,5:9)", ["a[0:3, 4:9]"],
    "a is 5x5, so columns 5..9 resolve to the single column 5.")
row(13, "a([2,4,5],[1,3])", ["a[np.ix_([1, 3, 4], [0, 2])]"])
row(14, "a(3:2:21,:)", ["a[2:21:2, :]"])
row(15, "a(1:2:end,:)", ["a[::2, :]"])
row(16, "a(end:-1:1,:) or flipud(a)", ["a[::-1, :]"])
row(17, "a([1:end 1],:)", ["a[np.r_[:len(a), 0]]"])
row(18, "a.'", ["a.transpose()", "a.T"])
row(19, "a'", ["a.conj().transpose()", "a.conj().T"])
row(20, "a * b", ["a @ b"])
row(21, "a .* b", ["a * b"])
row(22, "a./b", ["a/b"])
row(23, "a.^3", ["a**3"])
row(24, "(a > 0.5)", ["(a > 0.5)"])
row(25, "find(a > 0.5)", ["np.nonzero(a > 0.5)"])
row(26, "a(:,find(v > 0.5))", ["a[:, np.nonzero(v > 0.5)[0]]"])
row(27, "a(:,find(v>0.5))", ["a[:, v.T > 0.5]"])
row(28, "a(a<0.5)=0", ["a[a < 0.5] = 0", "a", "a = a_orig.copy()   # undo, so later rows see the original a"],
    "This row assigns in place, so a is restored afterwards.")
row(29, "a .* (a>0.5)", ["a * (a > 0.5)"])
row(30, "a(:) = 3", ["a[:] = 3", "a", "a = a_orig.copy()   # undo again"],
    "Also in place; a is restored afterwards.")
row(31, "y=x", ["y = x.copy()", "y"])
row(32, "y=x(2,:)", ["y = x[1, :].copy()", "y"])
row(33, "y=x(:)", ["y = x.flatten()", "y"])
row(34, "1:10", ["np.arange(1., 11.)", "np.r_[1.:11.]", "np.r_[1:10:10j]"])
row(35, "0:9", ["np.arange(10.)", "np.r_[:10.]", "np.r_[:9:10j]"])
row(36, "[1:10]'", ["np.arange(1., 11.)[:, np.newaxis]"])
row(37, "zeros(3,4)", ["np.zeros((3, 4))"])
row(38, "zeros(3,4,5)", ["np.zeros((3, 4, 5))"])
row(39, "ones(3,4)", ["np.ones((3, 4))"])
row(40, "eye(3)", ["np.eye(3)"])
row(41, "diag(a)", ["np.diag(a)"])
row(42, "diag(v,0)", ["np.diag(v, 0)"])
row(43, "rng(42,'twister'); rand(3,4)",
    ["from numpy.random import default_rng", "rng = default_rng(42)", "rng.random((3, 4))"])
row(44, "linspace(1,3,4)", ["np.linspace(1, 3, 4)"])
row(45, "[x,y]=meshgrid(0:8,0:5)",
    ["np.mgrid[0:9., 0:6.]", "np.meshgrid(np.r_[0:9.], np.r_[0:6.])"])
row(46, "(best way to eval functions on a grid)",
    ["np.ogrid[0:9., 0:6.]", "np.ix_(np.r_[0:9], np.r_[0:6])"],
    "The table prints np.ix_(np.r_[0:9.],np.r_[0:6.] - a missing paren, and float "
    "indices raise IndexError. Integer ranges are used here.")
row(47, "[x,y]=meshgrid([1,2,4],[2,4,5])", ["np.meshgrid([1, 2, 4], [2, 4, 5])"])
row(48, "(best way to eval functions on a grid)", ["np.ix_([1, 2, 4], [2, 4, 5])"])
row(49, "repmat(a, m, n)", ["np.tile(a, (m, n))"])
row(50, "[a b]", ["np.concatenate((a, b), 1)", "np.hstack((a, b))",
                  "np.column_stack((a, b))", "np.c_[a, b]"])
row(51, "[a; b]", ["np.concatenate((a, b))", "np.vstack((a, b))", "np.r_[a, b]"])
row(52, "max(max(a))", ["a.max()", "np.nanmax(a)"])
row(53, "max(a)", ["a.max(0)"])
row(54, "max(a,[],2)", ["a.max(1)"])
row(55, "max(a,b)", ["np.maximum(a, b)"])
row(56, "norm(v)", ["np.sqrt(v @ v)", "np.linalg.norm(v)"])
row(57, "a & b", ["np.logical_and(a, b)"],
    "The table writes a bare logical_and; it lives in the np namespace.")
row(58, "a | b", ["np.logical_or(a, b)"])
row(59, "bitand(a,b)", ["ai & bi"],
    "Bitwise operators need integer arrays, so the integer pair ai, bi is used.")
row(60, "bitor(a,b)", ["ai | bi"], "Same as row 59.")
row(61, "inv(a)", ["linalg.inv(a)"])
row(62, "pinv(a)", ["linalg.pinv(a)"])
row(63, "rank(a)", ["np.linalg.matrix_rank(a)"])
row(64, "a\\b", ["linalg.solve(a, b)", "linalg.lstsq(a, b)"])
row(65, "b/a", ["linalg.solve(a.T, b.T).T"],
    "The table says 'Solve a.T x.T = b.T instead'; that is written out here.")
row(66, "[U,S,V]=svd(a)", ["U, S, Vh = linalg.svd(a); V = Vh.T", "U", "S", "V"])
row(67, "chol(a)", ["linalg.cholesky(spd)"],
    "Cholesky needs a positive definite matrix, so spd = a @ a.T + 5I is used.")
row(68, "[V,D]=eig(a)", ["D, V = linalg.eig(a)", "D", "V"])
row(69, "[V,D]=eig(a,b)", ["D, V = linalg.eig(a, b)", "D", "V"])
row(70, "[V,D]=eigs(a,3)", ["D, V = eigs(a, k=3)", "D", "V"],
    "eigs comes from scipy.sparse.linalg and needs k < n-1.")
row(71, "[Q,R]=qr(a,0)", ["Q, R = linalg.qr(a)", "Q", "R"])
row(72, "[L,U,P]=lu(a)", ["P, L, U = linalg.lu(a)", "P", "L", "U", "np.allclose(a, P @ L @ U)"])
row(73, "conjgrad", ["cg(spd, v)"],
    "cg is scipy's conjugate gradient solver; it needs an SPD system.")
row(74, "fft(a)", ["np.fft.fft(a)"])
row(75, "ifft(a)", ["np.fft.ifft(a)"])
row(76, "sort(a)", ["np.sort(a)", "a.sort(axis=0); a", "a = a_orig.copy()   # sort is in place"])
row(77, "sort(a, 2)", ["np.sort(a, axis=1)", "a.sort(axis=1); a", "a = a_orig.copy()"])
row(78, "[b,I]=sortrows(a,1)", ["I = np.argsort(a[:, 0]); b = a[I, :]", "I", "b"])
row(79, "x = Z\\y", ["Z = a; y = v   # rebind, rows 31-33 reassigned x and y",
                     "x = linalg.lstsq(Z, y)", "x"])
row(80, "decimate(x, q)", ["sig", "signal.resample(sig, int(np.ceil(len(sig)/q)))"],
    "np.ceil returns a float; resample needs an int, so int(...) is applied.")
row(81, "unique(a)", ["np.unique(a)"])
row(82, "squeeze(a)", ["np.zeros((1, 3, 1, 4)).squeeze()", "np.zeros((1, 3, 1, 4)).squeeze().shape"],
    "a has no singleton dimensions, so a 1x3x1x4 array is used to show the effect.")

print(f"\n--- End of Task 2: {_n} cells, all 82 table rows covered. " + "-" * 20)
