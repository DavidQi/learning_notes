# If you want to know SnowFlake

[SNOWFLAKE ARCHITECTURE] (https://www.snowflake.com/product/architecture/)

[Snowflake Documentation] (https://docs.snowflake.com/en/index.html)

# Basic

```sql

describe table {table_name};

SHOW COLUMNS in {table_name};

alter table {table_name} add column {col_name} {col_type} (varchar|int|boolean|etc.);

alter table {table_name} rename column {old_col_name} to {new_col_name};

alter table {table_name} drop column {col_name};

alter table {table_name} rename to {new_table_name};

select get_ddl ('table', '{table_name}');

```

# Snowflake with S3 csv 

1、**normal**

```sql
-- Copy data directly into an exisging table
copy into 's3://{bucket}/backup/data_backup.csv'
from
(
    select * from A, B where A.a_id = B.b_id
)
CREDENTIALS = (AWS_KEY_ID = '',
                AWS_SECRET_KEY = '',
                AWS_TOKEN = ''
              )
file_format=(
              type = CSV
              --skip_header = 1
              --field_delimiter = '|'
              FIELD_OPTIONALLY_ENCLOSED_BY = ''''
              encoding=UTF8
              compression=gzip
            )
header = true
overwrite = true
single = true
max_file_size=5368709120;


-- Create a data stage and create a new table with data or copy date from the stage into an existing table
create or replace stage {stage_table_name}
    URL = 's3://{bucket}/backup/data_backup.csv'
    CREDENTIALS = (AWS_KEY_ID = '',
                AWS_SECRET_KEY = '',
                AWS_TOKEN = ''
              )
    file_format=(
          type = CSV
          skip_header = 1
          --field_delimiter = '|'
          empty_field_as_null = True
          null_if = 'NULL'
          FIELD_OPTIONALLY_ENCLOSED_BY = ''''
          encoding=UTF8
          compression=gzip
        );


-- create a new table with data 
create or replace table {table_name}
as 
select 
$1:: varchar as col_1,
$2:: int as col2
from @{stage_table_name}


-- copy date from the stage into an existing table
copy into {table_name}
    from {stage_table_name}
```

2、**snowpipe**

```sql
use role snowpipe_role;
use database snowpipe;

create or replace stage snowpipe.public.snowstage
    url='s3://snowpipe-demo/'
    credentials = (AWS_KEY_ID = '...' AWS_SECRET_KEY = '...' );
show stages;

-- Create target table for JSON data
create or replace table snowpipe.public.snowtable(jsontext variant);
show tables;

-- Create a pipe to ingest JSON data
create or replace pipe snowpipe.public.snowpipe auto_ingest=true as
    copy into snowpipe.public.snowtable
    from @snowpipe.public.snowstage
    file_format = (type = 'JSON');
show pipes;
```

# Snowflake with Python Pandas

```python

  from sqlalchemy import create_engine
  from snowflake.sqlalchemy import URL


  sf_engine = create_engine(URL(account='',
                                user='',
                                password='',
                                role='data_engineer',
                                warehouse='',
                                database='',
                                schema=''
                                )
                            )


  with sf_engine.connect() as con:
      df = pd.read_sql(sql, con=con)
      df.to_sql(name=table_name, con=con, if_exists="replace|append", index=False)
```
