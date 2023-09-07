<!-- Register.svelte -->
<script>
    import { createEventDispatcher } from 'svelte';
   
   const dispatch = createEventDispatcher();
   
  let username = "";
  let password = "";
  let password2 = "";
  let email = "";
  let errorMessage = ""; // Variable to hold the error message
  
   
   function handleRegistration(event) {
     event.preventDefault();
   
     // Benutzerdaten
     const userData = {
       username,
       password,
       password2,
       email
     };
   
     // HTTP-Anfrage senden
     fetch('http://127.0.0.1:8000/api/user/create/', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify(userData)
  })
    .then(response => {
      if (response.ok) {
        return response.json(); // Parse response as JSON
      } else {
        throw response.json(); // Parse error response as JSON
      }
    })
    .then(data => {
      alert("Registration successful!");
      // Extract user information from the response
      const { username, email, is_mediathekar } = data;
      // Perform further actions with the user information
    })
    .catch(error => {
      error.then(jsonError => {
        let errorMessage = "Registration failed: ";
        if (jsonError.username) {
          errorMessage += jsonError.username[0];
        } else if (jsonError.non_field_errors) {
          errorMessage += jsonError.non_field_errors[0];
        } else if (jsonError.password) {
          errorMessage += jsonError.password[0];
        } else if (jsonError.email) {
          errorMessage += jsonError.email[0];
        } else {
          errorMessage += error.message;
        }
        alert(errorMessage);
      });
    });
  }
  
   
   function redirectToLogin(event) {
     event.preventDefault();
     dispatch('showLogin', {});
   }
   </script>
   
   <style>
    .PageContent{
      display:flex;
      flex-direction: column;
      background-image: url('space.jpg');
      height: 100vh;
      background-size: cover;
      background-position: center center;
    }

     .container {
       width: 300px;
       margin: 0 auto;
       padding: 20px;
       background-color: #f5f5f5;
       border-radius: 5px;
       border: 1px solid #ddd;
       position: relative;
     }
   
     h2 {
      text-align: center;
      margin-bottom: 20px;
      padding-top: 10px;
    color: #0e2f65;
    font-family: "Ubuntu", sans-serif;
    font-weight: bold;
    font-size: 23px;
     }
   
     form {
       display: flex;
       flex-direction: column;
     }
   
     .input-group {
       display: flex;
       flex-direction: column;
       margin-bottom: 10px;
     }
   
     label {
      font-weight: bold;
    text-align: left;
    font-size: 12px;
    margin-bottom: 5px;
    color: #697692;
     }
   
     input[type="text"],
     input[type="password"],
     input[type="email"] {
       padding: 10px;
       border-radius: 5px;
       border: 1px solid #ddd;
     }
   
     button[type="submit"] {
      cursor: pointer;
    border-radius: 2em;
    color: #fff;
    background: linear-gradient(to right, #0e2f65, #1a61a3);
    border: 0;
    padding-left: 40px;
    padding-right: 40px;
    padding-bottom: 10px;
    padding-top: 10px;
    font-family: "Ubuntu", sans-serif;
    margin-top: 10px;
    margin-bottom: 10px;
    margin-right: 10px;
    margin-left: 75px;
   
    font-size: 13px;
    box-shadow: 0 0 20px 1px rgba(0, 0, 0, 0.04);
     }
   
     button[type="submit"]:hover {
      background: linear-gradient(to right, #1a55b4, #2792f5);
     }
   
     p {
      text-align: center;
      color: #0e2f65;
    }
   
   </style>

   <div class="PageContent">
   <div class="MedaverseSymbol">
    <h3>
      <p style="text-align:center;"><img src="./public/mvlogotp.png" width="300" class="center" alt="MV-logo"></p>
  </h3>
  </div>
   <div class="container">
    <h2>Registration</h2>
    <form on:submit={handleRegistration}>
      <div class="input-group">
        <label for="username">Username</label>
        <input type="text" id="username" name="username" placeholder="Enter your username" bind:value={username}>
      </div>
      <div class="input-group">
        <label for="password">Password</label>
        <input type="password" id="password" name="password" placeholder="Enter your password" bind:value={password}>
      </div>
  <div class="input-group">
        <label for="password">Confirm Your Password</label>
        <input type="password" id="password2" name="password2" placeholder="Confirm Your Password" bind:value={password2}>
      </div>
   <div class="input-group">
        <label for="email">Email</label>
        <input type="email" id="email" name="email" placeholder="Enter your email" bind:value={email}>
      </div>
 
      <button type="submit">Register</button>
 
      <p>Already registered? <a href="aa" on:click={redirectToLogin}><b>Click here to login</a></p>
    </form>
  </div>
  </div>