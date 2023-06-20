# Appendix Proposal
Name: John Muller				
Group: 4.2A
Date Submitted:  March 29th, 2023.



The purpose of this document is to propose a project idea and specify the requirements that your project will meet. In turn, the lecturer will provide feedback and discuss any necessary revisions with you. Kindly keep with the proposal deadline as specified by your lecturer.
You are required to use Python to develop an NLP based application. You can choose your own scenario as long as you meet the requirements specified below. Keep in mind that the following requirements must be fulfilled in relation to one another (not in an unrelated manner) and that each one must make sense in the context in which it is used.
While not mandatory, iGaming students are highly encouraged to choose a scenario which is related to iGaming.

•	1 text/document acquisition method out of: text file/s, audio, web scraping, images (OCR)
•	Tokenization
•	Lemmatisation
•	Vectoriser (count or tfidf)
•	Similarity Measure or Sentiment Analysis
•	Producing some kind of result/analysis
•	Saving result/analysis in file
•	Research and implement 1 technology/concept in your program out of:
o	GUI desktop app using tkinter, PyQt5, or any other Python GUI framework
o	Web app (e.g. Flask)
o	The concept of synonyms/antonyms/hyponyms (using WordNet)
o	OOP
o	Image pre-processing prior to OCR (e.g. contrast enhancement and noise reduction)
o	Matplotlib for advanced data visualization

Write the title only of the scenario that you are going to implement. Title should be self-explanatory (e.g. an intelligent chatbot) 
Dark engines Artificial intelligence (DEAI) 
_________________________________________________________________________________



AA1.1 – Produce a requirements analysis (7 marks)

1.	Write a short paragraph outlining at least 1 high-level objective of your application. As part of your explanation, mention the typical user/s of your application.
(2 marks)

My NLP application aims to analyze customer reviews and feedback for online platforms and businesses, with the objective of improving customer satisfaction and identifying areas for improvement. Using Python and an OOP approach, the application will implement required functionalities such as text acquisition, tokenization, lemmatization, vectorization, and sentiment analysis using TFIDF. The application will use a REST API and a database to store and retrieve data and output a text file as required by the project. The front-end will utilize HTML, CSS, and JS, and may include non-required functionalities such as text summarization and a chatbot using prebuilt responses and ChatterBot or chat GPT 4 API.

2.	Which acquisition method will you use? (choose 1).

text file/s          audio             web scraping          images (OCR)

In case of text files, audio, images, specify source. Social media and/ or user specified input 

In case of web scraping, specify URL. ______________________________________________
(1 mark)


3.	Why are tokenization and lemmatization required in your application?  (2 marks)

In my proposed application, tokenization and lemmatization are required to preprocess the text data and convert it into a format that can be analyzed by the machine learning algorithms.

Tokenization is the process of splitting a text document into individual words or "tokens". This is important because it allows the application to analyze the frequency of individual words, and to identify patterns and relationships between words.

Lemmatization, on the other hand, is the process of reducing words to their base or root form. This is important because it reduces the total number of unique words that need to be analyzed, and it allows the application to more accurately analyze the meaning of a sentence by understanding the relationship between different forms of the same word.

For example, without lemmatization, the application may treat "run", "running", and "ran" as separate words, even though they have a similar meaning. By lemmatizing these words to their base form "run", the application can more accurately analyze the frequency and context of this word, and make more accurate predictions about the sentiment or meaning of a given text document. Overall, tokenization and lemmatization are essential preprocessing steps for any NLP application that aims to accurately analyze text data.

4.	Which type of Vectoriser will you use and why?

For my NLP-based application, I have decided to use TF-IDF (Term Frequency-Inverse Document Frequency) as the vectorizer. This decision was made because TF-IDF is a widely used technique for text analysis and can effectively represent text data in a high-dimensional space, which can be used for various NLP tasks such as sentiment analysis and text classification.

TF-IDF takes into account the frequency of a term in a document and in the entire corpus of documents, allowing the algorithm to assign higher weights to terms that are more important in a particular document. This is particularly useful for my application because it will be analyzing customer reviews and feedback, where identifying key phrases and sentiments is important for understanding customer satisfaction and identifying areas for improvement.

Overall, I believe that TF-IDF is a suitable vectorizer for my application as it can effectively handle the type of text data that will be analyzed and provide meaningful insights for businesses looking to improve their customer satisfaction. 
(1 mark)



5.	Choose 1 out of:  Similarity Measure          Sentiment Analysis

More detail (how and why) about above choice:
Sentiment analysis is a natural language processing technique that involves analyzing and classifying textual data into categories based on the underlying sentiment, such as positive, negative, or neutral. In the context of my application, sentiment analysis will be used to analyze customer reviews and feedback to identify the overall sentiment towards a product or service. This will allow businesses to better understand customer needs and improve customer satisfaction.

Sentiment analysis can be implemented using various machine learning algorithms, such as support vector machines (SVMs), Naive Bayes, and neural networks. In my application, I will use a supervised learning approach with a pre-trained model and labeled data to classify the sentiment of text inputs. I will use the TFIDF vectorizer to extract features from the text, and then train the model to classify the sentiment of the text as either positive, negative, or neutral. This will be achieved by assigning a numerical value to each class and using the classification algorithm to predict the most appropriate class for each input.

Overall, sentiment analysis is a powerful tool that can help me improve customer satisfaction and identify areas for improvement. By accurately classifying customer feedback, businesses can take targeted action to address issues and improve customer experience.
(1 mark)

AA2.1 – Produce a planning document (7 marks)

6.	What will be the output of your application? What will you save in the file?
The output of my application will be in the form of responses to user queries, such as confirmation of a booking for a certain day or whether a particular product is offered. These responses will be provided to the user through various platforms such as Google Maps, Facebook, Instagram, or via my front-end dashboard. The application will also store these responses in a database, and they will be outputted in a text file as required by the project.

(1 mark)

7.	Choose 1 out of: 
GUI       WebApp        WordNet     OOP   Img Processing   Visualisation
	
More detail (how and why) about above choice:
My application will utilize a REST API built with a Django in Python OOP approach to perform natural language processing tasks such as text acquisition, tokenization, lemmatization, and sentiment analysis. For the GUI, the application will use a web app using React, which will allow users to easily access the application from any device with an internet connection. The web app will provide a user-friendly interface that allows users to input text, view results, and interact with the chatbot. Overall, the choice of a web app as the GUI aligns with the goal of creating a user-friendly and accessible solution. 
(2 marks)

8.	Mention 2 things you will do in your program to make it more user-friendly.
1	Error Handling: Implementing proper error handling can greatly improve user experience by providing clear and concise error messages. Instead of just crashing or showing a generic error message.
So, my app should inform the user of what went wrong and how to fix it.
2	Documentation: Providing clear documentation, either through in-app help menus or external documentation, can greatly improve the usability of my program. 
The users should be able to understand what the program does, how to use it, and what they can expect from it.


3	Interface: One way to make the application more user-friendly is to focus on implementing an intuitive and user-friendly interface. By doing so, users will be able to easily navigate and interact with the application, which can enhance their overall experience and satisfaction.

(2 marks)

9.	List 2 practical uses of your application (as it is or with slight modifications)

1	Customer feedback analysis: The application's natural language processing capabilities could be used to analyze customer reviews and feedback for businesses across various industries such as hospitality, retail, or healthcare. By analyzing the sentiment of the feedback, businesses could identify areas of improvement and take action to improve customer satisfaction.
2	Chatbot for customer service: The application's ability to respond to user queries and bookings could be leveraged to create a chatbot for customer service. This chatbot could be integrated into a business's website or social media platforms to provide customers with quick and automated responses to their queries. This would improve the efficiency of the customer service process and reduce the workload of customer service representatives.




The required functionalities for the project are 

1. chatbot for platform
2. Content analysis (text mining)

The None required functionalities are
3. Text summarization (abstractive)
4. Sentiment analysis (opinion mining)
5. Text classification ?

