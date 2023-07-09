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
- Stratify -> class_weight (class 1에 가중치 부여)
- sklearn.utils.class_weight.compute_class_weight
- sklearn.utils.class_weight.compute_sample_weight

## current result
- ACC = 60.09%
- Elapsed Time: 18.0 min 55.79 sec