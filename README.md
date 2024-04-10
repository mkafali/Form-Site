# Form Site

**This is my form creation website project that I created while learning Django and Javascript.**<br>
**This project includes 5 apps: Users, Appforms, Questions, Answers, Results.**

## Users
**Users app is related to user and profile actions like:**
* Log in/ Log out
* Register
* Profile Edit
* User Settings
* Search Form with Form Code
* Dark Mode: If user is authenticated, their dark mode preferences are stored in database. If not, the user's dark mode preferences are stored in Local Storage. 
* I prevented security vulnerabilities as much as possible for each feature in the backend through various controls.

## Appforms

This app handles form operations. Each form has certain attributes: author, slug, title, questions, anonymous, filled_by, code, ask_code, form_code, completed, is_changed, changed_time. Author indicates the owner of the form. Slug acts as the id of the form. Title is the title of the form. Questions contain the questions included in the form. Anonymous specifies whether the form can be filled anonymously. filled_by contains the users who filled the form (if the form allows anonymous filling, users are not recorded in filled_by). form_code is the code of the form. When searching, you access the form using this code. ask_code indicates whether a password is required to access the form. This password is the code in the form's code attribute. If the code is unknown, access to the form page is not possible.

**Form Creation:**<br>
You can dynamically add and delete questions. There are 4 types of questions: Open Ended, Optional, Multi Choice, Rank. Each question is treated differently. If Open Ended is selected, you are not asked to add options. In other cases, a field is dynamically opened with JavaScript for you to add options. Just like for questions, you can add as many options as you want with JavaScript. You can determine in which order the questions will be shown to the user by giving any number you want to the desired question. You can decide whether each question must be answered. 
You can decide on the title of the form, whether the form can be filled out anonymously, and whether a code will be required when accessing the form page. In addition to questions, many controls are made with JavaScript. For example, question numbers cannot be negative or zero, and question numbers must follow a certain order. In a form containing a total of 5 questions, there should not be a question numbered 22. If nothing is entered in dynamically created question or option fields, these fields should be deleted so that no data is sent from the back end. All of these are done with JavaScript. In addition to these, there are some JavaScript codes that make both the user's and the developer's job easier.

In the back end, many things related to the form are rechecked to ensure that the form is created correctly and to ensure security. Data coming from the template is interpreted and processed appropriately. In this context, the questions and answers written by the user are saved according to the question number. It is also indicated in the database which form each question belongs to.

**Form Page:**<br>
Depending on whether a code is requested, it asks for a code. If it's unknown, access to the content is denied. When accessing the content, if the form doesn't allow anonymous filling and has been previously answered, the user's answers to the questions are displayed on the screen. If the user wants to change, answer, or delete some answers, they can do so by pressing the "edit answer" button. JavaScript ensures that the user cannot interfere with old answers without pressing this button. If the questions have not been answered before, the user can directly answer the questions and submit them if form cannot be filled anonymously. However, if the form creator specified some questions as mandatory to fill in, the user cannot complete the form or edit the answers without answering these questions. If the form can be filled anonymously, the users' answers are saved, but it's not indicated who filled the form. When the user fills out the form and revisits the form site, they cannot see their old answers. If they fill out the form again, their old answers are deleted. If the form can be filled anonymously, the form can be filled out without logging in. In this case, the user can repeatedly answer the form, and each filling process is considered a new response. To prevent this, I use COOKIES. This way, if an unauthenticated user fills out the form and tries to submit it again, their old answers are deleted. Additionally, information is provided that the form has been filled out, just like for a logged-in user. Also, many JavaScript controls work for the form to be filled out as desired. For example, mandatory questions must be answered before submitting the answers. In addition to these, there are also functional JavaScript codes. For example, in questions of type "Rank," you can rank the options by dragging and dropping them among themselves.

Form Submit in the back end involves many checks to ensure that the form is created correctly and to ensure security. Data coming from the template is interpreted and processed appropriately. If the checks are successful, the user's answers are saved associated with the relevant question. Depending on whether the form can be filled anonymously, the username is saved in the list of those who filled out the form. If the form is anonymous and there is a response from an unauthenticated user, the response is saved. It's indicated through COOKIES that the user filled out the relevant form. If the answers are changed, i.e., if they are resubmitted, the following paths are followed:
1- If the form cannot be filled anonymously, the user's old answers are compared with the new answers. If something remains unchanged, that answer is not touched. If an answer is deleted, that answer is deleted. If an answer is changed, the relevant answer is updated. If a previously unanswered question is answered, a new answer is created.
2- If the form can be filled anonymously and the user is authenticated, the user's answers are searched among the previous answers, and all these previous answers are deleted, and new answers are saved. If the user is not authenticated, data is retrieved from COOKIES, and it's checked whether the user has previously answered or not. If they have answered, the relevant answers are deleted, and new answers are added.

**Form Edit:**<br>
You can add and delete questions, and change the numbers of the questions. If a question is deleted, the answers to that question are also deleted. Additionally, you can make changes related to the form itself. For example, whether the form can be filled anonymously, whether a password is required when entering the form site, the title of the form, etc. Furthermore, the form can be marked as complete. This means that no one can fill out the form anymore. Except for completing the form, every action taken is logged, and the user is informed about the changes made to the form and when they were made on the form page. This prevents the form owner from manipulating the data easily. If the form is completed, when entering the form site, the user is informed that the form has been completed. The user can only view the questions and answers but cannot submit them. In the back end, many operations and checks are performed. The relevant changes are saved, the is_changed property of the form is set to True, and the changed_time is recorded as the current time.

## Questions
Each question object has some attributes: 
* belongs_to --> Identify the form to which this question belongs.
* question --> Question.
* slug --> Question SLug. It is like id of question.
* number --> Number of question.
* type --> It could be Optional, Open Ended, Multi Choices, Rank.
* options --> It will be empty if type is Open Ended.
* required --> If it is True, then this question must be answered by the user.
* answers --> Answers of this question.

## Results
The result page processes and presents the data obtained from each form response. To collect this data, I used the Fetch API. There are three types of result: General results, Graphs, and People's answers.

For the first type, General results, which includes optional and multiple-choice questions, the answers are fetched using the Fetch API. The number of responses for each option is calculated, sorted, and presented to the user. Additionally, a percentage is calculated based on how often each option is chosen, and this information is also presented to the user. In the case of MultiChoice and Optional questions, users' responses are gathered and processed. The options are then sorted based on the average ranking given by the users. The option with the highest average ranking is placed first, while the lowest-ranked option is placed last.

The second type of result is Graphs, where I utilized Google Charts to present the general situation of responses to optional and multiple-choice questions using column charts and pie charts.

The third type, People's answers, displays the responses of each user who filled out the form. For this, the names of the respondents are collected, and a button is created for each name. When a user's button is clicked, their responses are fetched using the Fetch API, processed, and presented to the user.

It's worth noting that in forms where responses can be submitted anonymously, no data is fetched for the People's answers section since the identities of the respondents are not recorded; only their responses are saved. Therefore, the General results and Graphs sections still function properly.

## Note 
In this project, I used some things for the first time: JavaScript (I had never used JavaScript in a real project before), JSON, DOM manipulations, Cookies, Local Storage, Fetch API, Asynchronous programming, Promises, google.charts, and some JavaScript features. Therefore, this project was very helpful in improving my JavaScript skills.
