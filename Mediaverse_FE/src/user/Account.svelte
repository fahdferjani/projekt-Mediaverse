<script>
  import { onMount } from 'svelte';
    import { createEventDispatcher } from 'svelte';
  
    let token;
    let username;
    let email;
    let isMediathekar;
    let newUsername = '';
    let newEmail = '';
    let newPassword = '';
    let confirmPassword = '';
    let updateErrorMessage = '';
  
    const dispatch = createEventDispatcher();
  
    onMount(async () => {
      // Retrieve the token from localStorage
      token = localStorage.getItem('token');
  
      // Perform API call to get user info
      try {
        const response = await fetch('http://127.0.0.1:8000/api/user/me/', {
          headers: {
            Authorization: `Token ${token}`
          }
        });
  
        if (response.ok) {
          const data = await response.json();
          username = data.username;
          email = data.email;
          isMediathekar = data.is_mediathekar;
        } else {
          throw new Error('Failed to fetch user information');
        }
      } catch (error) {
        console.error(error);
      }
    });
  
    async function updateUser(event) {
      event.preventDefault();
  
      const updatedUserData = {
        username: newUsername || username,
        email: newEmail || email,
        password: newPassword,
        password2: confirmPassword
      };
  
      try {
        const response = await fetch('http://127.0.0.1:8000/api/user/me/', {
          method: 'PATCH',
          headers: {
            'Content-Type': 'application/json',
            Authorization: `Token ${token}`
          },
          body: JSON.stringify(updatedUserData)
        });
  
        if (response.ok) {
          alert('Account information updated successfully');
        } else {
          throw await response.json();
        }
      } catch (error) {
        let errorMessage = 'Failed to update account information: ';
        if (error.username) {
          errorMessage += error.username[0];
        } else if (error.email) {
          errorMessage += error.email[0];
        } else if (error.password) {
          errorMessage += error.password[0];
        } else if (error.non_field_errors) {
          errorMessage += error.non_field_errors[0];
        } else {
          errorMessage += error.message;
        }
        updateErrorMessage = errorMessage;
      }
    }
  
  </script>
  
  <main>
    <div class="box1">
      <h1>Account Information</h1>

      <div class="account-info">
        <div class="card">
          <div class="card-left">
            <div class="image">
              <img src="aiface.jpg" alt="" class="profile-pic">
            </div>
          </div>
          <div class="card-right">
            <h2>Username: {username}</h2>
            <p class="title">User Status: {isMediathekar ? 'Mediathekar' : 'User'}</p>
            <p>Email: {email}</p>
          </div>
        </div>
      </div>
    </div>

    <div class="update-info">
      <h1>Change Information</h1>
      <div class="card2">
        <form on:submit={updateUser}>
          <div class="form-group">
            <label for="newUsername">New Username:</label>
            <input type="text" id="newUsername" bind:value={newUsername} />
          </div>
          <div class="form-group">
            <label for="newEmail">New Email:</label>
            <input type="email" id="newEmail" bind:value={newEmail} />
          </div>
          <div class="form-group">
            <label for="newPassword">New Password:</label>
            <input type="password" id="newPassword" bind:value={newPassword} />
          </div>
          <div class="form-group">
            <label for="confirmPassword">Confirm Password:</label>
            <input type="password" id="confirmPassword" bind:value={confirmPassword} />
          </div>
          {#if updateErrorMessage}
          <p class="error-message">{updateErrorMessage}</p>
          {/if}
          <button type="submit">Confirm Changes</button>
        </form>
      </div>
    </div>
  
  </main>
  
  <style>
    main {
      margin: 0;
      padding: 0;
      padding-bottom: 1rem;
      height: 750px;
      width: cover;
      font-family: "Helvetica", sans-serif;
      line-height: 1.2em;
      background: linear-gradient(to right, #180b61, #b73ce7, #23A6D5, #23D5AB);
      justify-content: center;
      color: #dce4ec;
      line-height: 1.5;
      display: flex;
      align-items: center;
    }
    
    .card {
      box-shadow: 0 4px 8px 0 rgba(0, 0, 0, 0.7);
      background: rgba(250, 247, 247, 0.5);
      max-width: 800px;
      height: 438px;
      text-align: left;
      font-family: arial;
      display: flex;
      align-items: center;
    }
  
    .card-left {
      padding: 1rem;
    }
  
    .card-right {
      padding: 1rem;
      text-align: left;
    }
  
    .card2 {
      box-shadow: 0 4px 8px 0 rgba(0, 0, 0, 0.7);
      background: rgba(250, 247, 247, 0.5);
      max-width: 800px;
      height: 500px;
      text-align: left;
      font-family: arial;
      display: flex;
      align-items: center;
    }
  
    .form-group {
      display: flex;
      align-items: center;
      text-align: center;
      justify-content: center;
    }
  
    .form-group label {
      height: 58.4px;
      width: 190px;
    }
  
    .title {
      color: rgb(73, 73, 73);
      font-size: 18px;
    }
  
    .account-info {
      margin-right: 1rem;
    }

    .update-info {
      justify-content: center;
        color: #dce4ec;
        height: 700px;
        text-align: center;
    }
  
    button {
      border: none;
      outline: 0;
      display: inline-block;
      padding: 8px;
      color: #e0e6eb;
      background: linear-gradient(to right, #08243c, #185792);
      text-align: center;
      cursor: pointer;
      width: 132%;
      font-size: 18px;
    }
  
    button:hover {
      opacity: 0.7;
    }

    .image{
      position: relative;
      height: 250px;
      width: 250px;
    }

    .image .profile-pic{
        width: 100%;
        height: 100%;
        object-fit: cover;
        border-radius: 50%;
        box-shadow: 0 5px 20px rgba(0,0,0,0.4);
    }

    .input-group input[type="text"],
    .input-group input[type="email"],
    .input-group input[type="password"] {
      width: 100%;
    }
    
    .box1 {
        justify-content: center;
        color: #dce4ec;
        height: 700px;
        text-align: center;
    }
  
    h1 {
      color: #e5e5e6;
      padding-top: 3rem;
      size: 3rem;
    }
  
    h2 {
      color: #08243c;
      padding-top: 3rem;
      size: 3rem;
    }
  
    label {
      color: #08243c;
      padding-top: 3rem;
      size: 3rem;
    }
  
    p {
      color: #08243c;
      padding-top: 1rem;
    }

  </style>