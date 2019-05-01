Programdom
===========

.. image:: https://travis-ci.com/vCra/Programdom.svg?token=fL2aJPJ1Aobzg5cofH7d&branch=master
    :target: https://travis-ci.com/vCra/Programdom

.. image:: https://api.codeclimate.com/v1/badges/22c1c4868a13d298bea2/maintainability
   :target: https://codeclimate.com/repos/5cb1f27f7ed2ee131c001905/maintainability
   :alt: Maintainability

.. image:: https://api.codeclimate.com/v1/badges/22c1c4868a13d298bea2/test_coverage
   :target: https://codeclimate.com/repos/5cb1f27f7ed2ee131c001905/test_coverage
   :alt: Test Coverage

.. image:: https://img.shields.io/github/license/vCra/Programdom.svg
   :target: https://github.com/vCra/Programdom/blob/master/LICENSE


Programdom is an application that lets lecturers test their students understanding of coding concepts. How does it work?
 - A Lecturer creates a coding problem, with some skeleton code and test cases.
 - The lecturer adds a problem to a workshop that they can present
 - Students join the workshop via a code, and attempt to solve the problem, by changing the code
 - Students get given feedback on what tests pass and fail
 - Lectuers see results live as they are submitted

Under the hood, we are using Judge0 in order to evaluate each submission.

Usage
-----

If you want to run Programdom locally, then great! All you need to do is the following:

1. Ensure you have docker and docker-compose installed and usable

2. Run ``docker-compose -f prod.yml up``

3. Wait for the image to build, and then access the instance at localhost:80

In order to actually use the system, they are some "first steps" that should be run

1. Create a super user - ``docker-compose -f prod.yml run python manage.py createsuperuser`` - answer the prompts for
your username and password

2. Import default programming languages. While languages can be created manually in Django Admin (accessible at ``/admin``), it's
normally easier to import the default ones. Run ``docker-compose -f prod.yml run python manage.py``


Usage in production
-------------------

In production, a few changes will need to be made.

1. Add your SSL keys to the nginx config file, which is in ``compose/nginx.conf``. At the same time, change
``server_name`` to the hostname of your server.

2. Create a Security Key - This can be done by changing the ``SECRET_KEY`` property in ``.envs/.prod/.django``

3. Create a secure username and password for postgres in ``.envs/.prod/.postgres``

4. Create a new secret and access key for minio in ``.envs/.prod/.minio``

5. Uncomment all of the security lines in ``config/settings/production.py``



Licence
-------

This software is released under the MIT License

Authors
-------

`programdom` was written by `Aaron Walker <aaw13@aber.ac.uk>`_.