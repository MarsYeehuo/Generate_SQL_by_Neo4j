# Generate_SQL_by_Neo4j

This is a small tool to generate SQL code with **LLM** and **Neo4j Graph Database**.

## Preparation
To use this toll you need a **SQL Database** and a **Neo4j Graph Database**.

To set up **Neo4j** please refere to the official webset <https://neo4j.com/>. Neo4j >= 5.0.0 is recommanded.

You need to set the link, user name and password for the **Neo4j** Database in the following code:

    from neomodel import config

    config.DATABASE_URL = 'bolt://USER_NAME:PASSWORD@localhost:7687/NEO4J_DATABASE_NAME'

## Database Structure For Neo4j

In the neo4j all knowledge is stored as a 'Unit', which contains a **Unit** node, a **NLP** node, an **EXPLANATION** node and a **Field** node. The **Unit** node has the attribute *uid* (e.g. unit_001). The **EXPLANATION** has the attribute *text*. The **NLP** node has the attribute *text*.

There are different **Relationships** connecting the nodes, you can refer to the following example:

    {Unit}-[EXPLAINS]->{EXPLANATION}
    {Unit}-[DESCRIBE_IN]->{NLP}
    {Unit}-[MAPS_TO]->{Field}

Meanwhile, there are **Relationships** connecting the **Table** and **Field** like:

    {Table}-[HAS_FIELD]->{Field}

When 2 different **Unit** is called in a same ture, there will be a new type of **Relationship** connecting them called **ASSOCIATED_WITH**.

## Running

To run the code locally, you can run the `main.py`.

To deploy this tool as a api, run

    uvicorn tool_api:app --host 0.0.0.0 --port 8081

in cmd.
