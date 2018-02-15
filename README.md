''' 
# Logs Analysis Project

Runs a logs analysis program on a dataset made up of website data for a news site. It then returns 3 queries that are relevant to the operation of the site. 

These are:

1) The most popular 3 articles of all time    
2) The most popular authors of articles of all time
3) Days where more than 1% of requests lead to errors

# Dependencies & Notes

VirtualBox/Vagrant environment is assumed in this README but essential components and their versions include: Python 3, PostgreSQL and the psycopg2 library. The newsdata.sql database that the queries operate upon is also provided in this repository.

# Installation & Setup

 1. Download the repository, and run it within a vagrant Virtual Machine. The exact setup that was used in this program was obtained from the udacity FSND-Virtual-Machine which had a PSQL console already installed.
 2. Run the newsdata.sql file to have the database create the data tables within the VM using this command in the VM. 
 	```
 	psql -d news -f newsdata.sql
 	```
 3. Create the below views of the data tables in the PSQL console of the VM.
 4. Run the logs.py program in python3 and the logs analysis questions should print to console.

# 1.) logs.py
This houses the program the calls the queries from the database in the virtual machine and then prints them to the console.

# 2.) newsdata.sql
This will create the data tables that the program draws from from within the Virtual Machine.

# SQL Audit Trail

## Log_Q2 - Audit Trail

### Creates a table connecting author ID, article titles, and views.

```
SELECT articles.author, articles.title, count(*) as views      
FROM articles
JOIN log      
ON articles.slug = (regexp_split_to_array(path,
E'/article/'))[2]      
WHERE path != '/'      
GROUP BY (regexp_split_to_array(path, E'/article/'))[2], articles.title, articles.author      
ORDER BY views DESC;
```

### Created a View for Author IDs and views

```
CREATE VIEW author_id_views AS 
SELECT articles.author, count(*) as views
FROM articles      
JOIN log      
ON articles.slug = (regexp_split_to_array(path, E'/article/'))[2]      
WHERE path != '/' 
GROUP BY (regexp_split_to_array(path, E'/article/'))[2], articles.author 
ORDER BY views DESC;
```

### Then Created the view author_total_views

```
CREATE VIEW author_total_views AS      
SELECT author, SUM(views) as views
FROM author_id_views      
GROUP BY author      
ORDER BY views DESC;
```

### Joined author table with author_total_views view-table

```
SELECT authors.name, author_total_views.views     
FROM authors, author_total_views     
WHERE authors.id = author_total_views.author     
GROUP BY authors.name, author_total_views.views     
ORDER BY views DESC     
LIMIT 3;
```

## Log_Q3 - Audit Trail

### Creating a view that holds the total number of errors made on a certain day

```
CREATE VIEW status_errors AS  
SELECT date(time), count(status) as errors  
FROM log  
WHERE status NOT LIKE '%200%'  
GROUP BY date(time);
```

#### So we first select the dates we had errors, then we also need to make a total of all requests on those days

```
CREATE VIEW total_requests AS 
SELECT date(time), count(status) as total 
FROM log 
GROUP BY date(time);
```

#### Than we join these two tables so that errors and total requests match up on the days errors occur and make another view

```
CREATE VIEW error_day_total AS 
SELECT status_errors.date, status_errors.errors, total_requests.total  
FROM status_errors, total_requests
WHERE status_errors.date = total_requests.date 
ORDER BY status_errors.date ASC;
```

#### Now to divide those total errors on those days by the total requests on those days to find the percentage and make this another view

```
CREATE VIEW error_percent AS 
SELECT date, (CAST(errors AS float) / CAST(total AS float)) * 100 as percent  
FROM error_day_total  
GROUP BY date, percent
ORDER BY date ASC;
```

#### Now take that view and filter out all the percentages that are not greater or equal to 1

```
SELECT date, percent FROM error_percent WHERE percent >= 1;
```
