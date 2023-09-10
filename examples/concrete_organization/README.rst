====================================
Building an app with concrete models
====================================

When you use "concrete models" in your app, you are using the models -
and the database tables - added by installing the `organizations`
Django app in your project. This is a simple (and often sufficient!)
way of integrating multi-user accounts into your Django project.

One consequence to be aware of in doing so is that all of your custom
model classes will use multi-table inheritance, which involves joining
tables to fetch data (where you have used your own class, that is).
Further, all of the relations will be between the concrete `organization`
models, e.g. between `organizations.Organization` and
`organizations.OrganizationUser`, for example, and not *directly* to your
own class implementations. Accessing these relations then requires an
additional attribute reference and database join.
