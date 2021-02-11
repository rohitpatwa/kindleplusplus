# kindle++

![Kindle diagram](https://github.com/rohitpatwa/kindleplusplus/blob/master/media/Kindle-111.jpg)

Revesit the wise/impactful lines you read from a book.

Ever happend that you read a wonderful book sometime ago, that book had a positive impact on you but, with time you forgot it's teachings you wish you could have rememembered. If yes, you're not alone. All of us go through similar situations more often than we think.

Try to remember your favourite book. Now list down 10 things which you appreciated the most in that book. Now repeat the activity for top 10 of your favorite books. Exhausting right?

Personal use was the starting motivation for this project. Upon sureveying random people, we came to realize that this problem is far more frequent that we ever expected.

We created a small service, which takes your kindle highlights and stores them in a database. Based on your selected frequency, we send you emails with your highlights with contextual information.

We always welcome ideas and feature requests.

## How to use

1. Open your book on your Amazon kindle device
2. Click on **Options > Notes > Export Notes**
3. You will receive an email from amazon titled **"Your Kindle Notes from \<book name\>"**. Forward that email to **"kinghuskier@gmail.com"**
4. You're all set
5. For any customizations requirements, please send an email to "kinghuskier@gmail.com" with "kindleplusplus" in the subject

## Internal Flow

Here is the step by step flow of how it works internally.

![Flow diagram](https://github.com/rohitpatwa/kindleplusplus/blob/master/media/flow.png)

## Technologies and Services Used

* Python3
* MongoDB
* NLTK
* Flask
* Heroku

## TODO

1. Add a UI for users to sign-up easily
  
2. Give users the capability to customize their email preferences

3. Scrape the book cover when parsing the notes

4. Add book cover to the email

## Author

* **Rohit Patwa** [\[LinedIn\]](https://www.linkedin.com/in/rohitpatwa/)
