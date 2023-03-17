# Calculadora ENEM

### Video Demo:  
<https://youtu.be/0IVnKBge6-U>

### Description:
In case you don't know, ENEM (High School National Exam) is the most important college entrance exam in Brazil. Calculadora ENEM is a web application via which you can calculate the simple and weighted average of your ENEM scores. You can also save your scores, weights of each subject, and results if you create an account. 

### app.py:
It contains the backend of the web application. It handles most of the data validations in each route, database queries, and modifications, generation of the web application's pages' contents, etc. Flask is used to render templates, flash warnings, access forms' data, store cookies, etc. Werkzeug security is used to store and check passwords safely. CS50 library is used to connect to the database. This file handles most of the web application logic.

### helpers.py:
It contains a function to make login required on certain pages, not letting non-registered users access features that require an account.

### calculadora.db:
It is the web application's database, in which information such as a user's saved scores, results, and weights, in addition to all the registered users and respective encrypted passwords, is stored.

### static/adicionar.js:
This script validates the form data when saving a new score or weight. It prevents the form from submitting if there are blanch fields or invalid values.

### static/module.mjs:
This script export to the other two scripts variables to be used, such as an array of all ENEM subjects, and two validation functions, one to validate the submitted scores and the other to validate the submitted weights.

### static/script.js:
This script calculates the simple and weighted average of the values submitted via the homepage form. It also shows those values on the page for the user, in addition to passing the calculator form data to the saving results form, allowing the user to save their results by clicking on the save button. It also refreshes the page (more specifically, redirects to the same page) when the clear button is clicked, clearing all data from the form.

### static/styles.css:
It contains a little of the stylization of the page, since Bootstrap is also used.

### templates/adicionar.html:
It's the template of the web application pages where the user can save or modify their scores and weights. It generates a different page depending on which one of those two the user selected.

### templates/cadastro.html:
It consists of the registration page and has a link to the login page.

### templates/index.html:
This template represents the homepage, where you can calculate the simple and weighted average and, if logged in, save your results. It has a link to the registration page and another to the login page if the user is not logged in.

### templates/layout.html:
This template consists of the layout of all the other templates. It has the HTML basic structure, in addition to including Bootstrap, Font Awesome, and static/styles.css in all templates. It also makes the navbar and the Flask flashing messages available in all templates. It's the basic structure of all templates.

### templates/login.html:
It consists of the login page and has a link to the register page, along with an "I forgot my password" link, which redirects the user to a page where they can change their password.

### templates/notas-e-pesos.html:
This file represents a page where the user can see, add, modify, and delete their scores and weights. It also allows them to use their saved scores and weights on the ENEM Calculator just by clicking on a button, without having to type them manually each time.

### templates/nova-senha.html:
It is the page where the user can change their password. If the user isn't logged in, it has a username input field. Otherwise, it uses the username stored in the session instead.

### templates/resultados.html:
It is the page where the user can see and delete their results. It has a link to the homepage, where the user can add more results. It also allows the user to use their saved results on the ENEM Calculator by clicking on a button, without having to type it manually.

### templates/sobre.html:
This file is a page with information about the ENEM, such as what is is, where you can see your scores, how you can use them to enter a university, etc. It also has links to official pages, where you can find more information about it.