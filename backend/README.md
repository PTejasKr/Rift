\# Xano Backend Setup Guide



This folder contains the schema and API definitions to bootstrap your SaaS backend in Xano. 



\## Step 1: Set up the Database

1\. Log in to Xano and create a new Workspace.

2\. Go to the \*\*Database\*\* tab.

3\. You can either manually create the tables using the `database\_schema.json` reference, or use Xano's "Import" feature if you convert the JSON to CSV. 

\*Note: Xano automatically generates standard `id` and `created\_at` fields. We have mapped our custom IDs to these.\*



\## Step 2: Establish Relationships (Table References)

In Xano, ensure you set up the following Table References (Foreign Keys):

\- In `Users` table: `org\_id` must point to `Organizations.id`

\- In `Events` table: `org\_id` must point to `Organizations.id`

\- In `Event\_Actions` table: `event\_id` must point to `Events.id`



\## Step 3: Set up Authentication

1\. Go to the \*\*API\*\* tab and add Xano's built-in \*\*Authentication\*\* extension.

2\. Ensure the `Users` table is selected as the authentication table.



\## Step 4: Generate API Endpoints

1\. In the \*\*API\*\* tab, click \*\*Add API Group\*\* (name it `v1`).

2\. Click \*\*Add API Endpoint\*\* -> \*\*CRUD Operations\*\*.

3\. Select all 4 tables (`Organizations`, `Users`, `Events`, `Event\_Actions`). Xano will instantly generate the GET, POST, PUT, and DELETE routes.

4\. Add the `user\_role` check (Admin/Manager) as Preconditions in your API function stack to enforce Role-Based Access Control.

