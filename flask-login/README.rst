Login with Flask-Login
======================

I've preferred put all into one source file but in production/more complex environments is 
obviously a good idea to split into the usual webapp/module/etc. structure.

Flask-Login uses SQLAlchemy as backend (sqlite to remain humble). A standard ``User`` table 
is created containing the must-have methods used by Flask-Login: ``is_active`` (always true 
as we don't need actrivated/deactivated users), ``get_id``, ``is_authenticated``.

The ``@login_manager.user_loader`` decorator is used to associate Flask-Login with the correct 
DB table (required).

The ``@login_manager.unauthorized_handler`` decorator is used to automatically redirect 
unauthorized users to a defined url (**/login** in this case).

The ``login()`` function is probably the most important one. It checks if the user exists in the 
database and then validates it as 'logged in' using the ``login_user`` function.
Likewise the ``logout()`` function does the exact opposite.

A ``private`` route has been setup just to demonstrate the ``@login_required`` decorator.

In this example there is very much room for improvements, such as password encryption, cookie
management ('Remember me'), and so on.

Give a look in the **template/** folder to check how to manage authentication from Jinja2 templates.

