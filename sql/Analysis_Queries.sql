-- select the database
use Apps_Dataset 
-- show all dataset columns & records
select * from Apps_Data 
-- EDA Queries
-- Total number of records 
select count(*) as num_records from Apps_Data 
-- Number of Apps by License_category
select License_category ,count(APP_NAME) as Num_apps from Apps_Data 
    group by License_category 
    order by Num_apps DESC 
-- Top continents by Number of Apps
select Contitent_name,count(APP_NAME) as Num_apps from Apps_Data
    where Contitent_name <> 'Unknown'
    group by Contitent_name 
    order by Num_apps DESC
-- Top continents by Number of free Apps
select Contitent_name,count(APP_NAME) as Num_apps_Free from Apps_Data
    where Contitent_name <> 'Unknown' and Pricing_type = 'Free'
    group by Contitent_name 
    order by Num_apps_Free  DESC 
-- Top(3) African countries by number of apps
select Top(3) Origin_country , count(APP_NAME) as Num_apps from Apps_Data
      where Contitent_name = 'Africa'
      group by Origin_country
      order by Num_apps  DESC 
-- Top(3) Asia countries by number of apps  
select Top(3) Origin_country , count(APP_NAME) as Num_apps from Apps_Data
      where Contitent_name = 'Asia'
      group by Origin_country
      order by Num_apps  DESC 
-- Top(3) Europe countries by number of apps 
select Top(3) Origin_country , count(APP_NAME) as Num_apps from Apps_Data
      where Contitent_name = 'Europe'
      group by Origin_country
      order by Num_apps  DESC 
-- Top(3) North America countries by number of apps 
select Top(3) Origin_country , count(APP_NAME) as Num_apps from Apps_Data
      where Contitent_name = 'North America'
      group by Origin_country
      order by Num_apps  DESC 
-- Top(3) Oceania countries by number of apps 
select Top(3) Origin_country , count(APP_NAME) as Num_apps from Apps_Data
      where Contitent_name = 'Oceania'
      group by Origin_country
      order by Num_apps  DESC 
-- Top(3) South America countries by number of apps 
select Top(3) Origin_country , count(APP_NAME) as Num_apps from Apps_Data
      where Contitent_name = 'South America'
      group by Origin_country
      order by Num_apps  DESC 
-- Free AI Chatbots Apps
select App_name ,Pricing_type from Apps_Data
     where App_type = 'AI Chatbot' and Pricing_type = 'Free'
-- Free AI Coding Assistant Apps
select App_name ,Pricing_type from Apps_Data
     where App_type = 'AI Coding Assistant' and Pricing_type = 'Free'
-- Free Calendar App Apps
select App_name ,Pricing_type from Apps_Data
     where App_type = 'Calendar App' and Pricing_type = 'Free'
-- Free Habit Tracker Apps
select App_name ,Pricing_type from Apps_Data
     where App_type = 'Habit Tracker' and Pricing_type = 'Free'
-- Top 5 Open Source License Types by Num_apps
select Top(5) License_type , count(APP_NAME) as num_apps from Apps_Data
    where License_category = 'Open Source'
    group by License_type 
    order by num_apps DESC  
-- Top 5 Proprietary License Types by Num_apps
select Top(5) License_type , count(APP_NAME) as num_apps from Apps_Data
    where License_category = 'Proprietary'
    group by License_type 
    order by num_apps DESC 
-- Pricing_categories by num_apps
select  Pricing_categories , count(APP_NAME) as num_apps from Apps_Data
    group by Pricing_categories
    order by num_apps DESC
-- Free Pricing_categories by num_apps
select  Pricing_type , count(APP_NAME) as num_apps from Apps_Data
    where Pricing_categories = 'Free'
    group by Pricing_type
    order by num_apps DESC
-- Freemium Pricing_categories by num_apps
select  Pricing_type , count(APP_NAME) as num_apps from Apps_Data
    where Pricing_categories = 'Freemium'
    group by Pricing_type
    order by num_apps DESC
-- Desktop app names
select App_name from Apps_Data 
    where Desktop = 'True'
-- Mobile app names
select App_name from Apps_Data 
    where Mobile = 'True'
-- web app names
select App_name from Apps_Data 
    where Web = 'True'
--------------------------------------------------
-- To connect to SQLserver in python 
select @@servername

