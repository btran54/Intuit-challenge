#### Setup Instructions:
1. Clone into local machine
2. Access the directory with `cd Intuit-challenge/asgn2`
2. Run with `python3 analyze_csv.py`

#### Sample Output:
```
Successfully loaded 9,355 rows


==================================================
Population Count by Experience Level
==================================================
                 Count Percentage
experience_level                 
Mid-level        1,869     19.98%
Senior           6,709     71.72%
Executive          281      3.00%
Entry-level        496      5.30%

Total: 9,355

==================================================
Total Salary by Experience Level
==================================================
                      Total Salary Percentage
experience_level                             
Mid-level          $219,652,203.00     15.62%
Senior           $1,089,247,250.00     77.47%
Executive           $53,239,079.00      3.79%
Entry-level         $43,913,249.00      3.12%

Grand Total: $1,406,051,781.00

==================================================
Employment Type Usage
==================================================
                Count Percentage
employment_type                 
Full-time       9,310     99.52%
Contract           19      0.20%
Part-time          15      0.16%
Freelance          11      0.12%

Most common employment type: Full-time (9,310 positions)

==================================================
Top Job Categories
==================================================

Top 7 job categories by count:
 1. Data Science and Research: 3,014 positions
 2. Data Engineering: 2,260 positions
 3. Data Analysis: 1,457 positions
 4. Machine Learning and AI: 1,428 positions
 5. Leadership and Management: 503 positions
 6. BI and Visualization: 313 positions
 7. Data Architecture and Modeling: 259 positions

Most common category: Data Science and Research (3,014 positions)

==================================================
Average Salary by Job Category
==================================================

Top 5 job categories by average salary:
1. Machine Learning and AI: $178,925.85
2. Data Science and Research: $163,758.58
3. Data Architecture and Modeling: $156,002.36
4. Cloud and Database: $155,000.00
5. Data Engineering: $146,197.66

==================================================
Additional Statistics
==================================================
Total positions: 9,355
Total salary pool: $1,406,051,781.00
Average salary: $150,299.50
Median salary: $143,000.00
Unique job titles: 125
Unique company locations: 70

==================================================
```