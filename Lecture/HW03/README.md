# OLS
<code>y = Xb + e</code>

- Estimate the unknown parameters (b) in linear regression model
- Minimizing the sum of the squares of the differences between the observed responses and the predicted by a linear function

## Optimization
- Need to minimize the error 
![](https://github.com/riverallzero/UNLV/assets/93754504/e3f86730-2bdb-4b4f-8df2-71a7ea08f21e)


- To obtain the optimal set of parameters (b), derivatives of the error w.r.t. each parameters must be zero.
  
![](https://github.com/riverallzero/UNLV/assets/93754504/f01bac09-c189-4285-a7cd-9581d194f156)

- For Code
  ```python
  np.linalg.pinv(X_train.T.dot(X_train)).dot(X_train.T).dot(y_train)
  ```

### numpy.linalg.inv vs numpy.linalg.pinv
- numpy.linalg.inv
  - In my dataset, occured <code>Sinular Matrix</code> error. This is because the inverse matrix cannot be obtained if ad-bc is 0, as shown in the expression below. Since numpy.linalg.inv computes the inverse of the input square matrix, if it does not have an inverse, LinAlgError will be thrown for Singular Matrix.

    ![image](https://github.com/riverallzero/UNLV/assets/93754504/540ce6fb-f45e-4b90-b99c-7ae5c74dd23b)

- numpy.linalg.pinv
  - This function computes the pseudo-inverse for an arbitrary matrix, so it will return a result even if the inverse does not exist.
