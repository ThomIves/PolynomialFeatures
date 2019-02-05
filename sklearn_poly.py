import LinearAlgebraPurePython as la 


max_range = 2

X = [[1*x for x in range(max_range)],
     [2*x for x in range(max_range)]]
     # [3*x for x in range(max_range)],
     # [4*x for x in range(max_range)],
     # [5*x for x in range(max_range)]]

X = la.transpose(X) # print(X)

# Fitting Polynomial Regression to the dataset
from sklearn.preprocessing import PolynomialFeatures
poly_reg = PolynomialFeatures(degree = 2)

X_poly_features = poly_reg.fit(X)
# print(X_poly_features)
# print()

# fit or fit_transform must be called before this is called
feature_names = poly_reg.get_feature_names()
feature_names.sort()
print(feature_names)
print()

# X_poly_transform = poly_reg.transform(X)
# print(len(poly_reg.get_feature_names()))
# print(X_poly_transform)
# print()

# print(poly_reg.get_feature_names())
# print()

# print(poly_reg.get_params())
# print()

# poly_reg.set_params(degree=3, interaction_only=True, include_bias=False)
# print(poly_reg.get_params())
# print()

# poly_reg.set_params(degree=2, interaction_only=False, include_bias=True)
# print(poly_reg.get_params())
# print()

# X_poly_full = poly_reg.fit_transform(X)
# print(X_poly_full)
# print()

# poly_reg.set_params(interaction_only=True)
# print(poly_reg.get_feature_names())