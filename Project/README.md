# Data

## description
| Column              | Description	                                  | Type |
|---------------------|-----------------------------------------------|------|
| income              | Income of the user                            | int  |
| age                 | Age of the user                               | int  |
| experience          | Professional experience of the user in years  | int  |
| profession	         | Profession	                                   | str  |
| married             | Whether married or single                     | str  |
| house_ownership	    | Owned or rented or neither                    | str  |
| car_ownership	      | Does the person own a car	                    | str  |
| current_job_years	  | Years of experience in the current job        | int  |
| current_house_years | Number of years in the current residence      | int  |
| city	               | City of residence                             | str  |
| state	              | State of residence                            | str  |
| risk_flag(target)   | Defaulted on a loan	                          | str  |

## label unbalanced
<img width="30%" alt="스크린샷 2023-07-09 오후 4 48 42" src="https://github.com/riverallzero/UNLV/assets/93754504/73362a1b-5cef-477a-be37-fba8fde91505">

- Stratify -> class_weight (class 1에 가중치 부여)
- sklearn.utils.class_weight.compute_class_weight
- sklearn.utils.class_weight.compute_sample_weight


## current result
### SVM
- AUC = 0.600
- Elapsed Time: 18.0 min 55.79 sec

### SVM with Spark
- AUC = 0.499
- Elapsed Time: 0.0 min 10.74 sec
