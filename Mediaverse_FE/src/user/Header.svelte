<!-- Header.svelte -->
<script>
  import { Link } from "svelte-navigator";
  import { onMount } from "svelte";

  let token;
  let username;
  let email;
  let isMediathekar;

  onMount(async () => {
    // Retrieve the token from localStorage
    token = localStorage.getItem("token");

    // Perform API call to get user info
    try {
      const response = await fetch("http://127.0.0.1:8000/api/user/me/", {
        headers: {
          Authorization: `Token ${token}`,
        },
      });

      if (response.ok) {
        const data = await response.json();
        // Extract user information from the response
        username = data.username;
        email = data.email;
        isMediathekar = data.is_mediathekar;
      } else {
        throw new Error("Failed to fetch user information");
      }
    } catch (error) {
      // Handle error
      console.error(error);
    }
  });
</script>

<main>
  {#if token}
    <header>
      <div class="logo">
        <img src="./Buch_logo_dunkeljpg.jpg" alt="" width="100px" />
      </div>
      <div class="ueberschrift">
        <h2>Mediaverse</h2>
      </div>

      <div class="box">
       
        <nav>
          <ul>
          <li><Link to="/"><button>Search</button></Link></li>
          <li><Link to="FavList"><button>Favourites</button></Link></li>
          <li><Link to="ResourcesList"><button>Resource History</button></Link></li>
          {#if isMediathekar}
          <li><Link to="CreateResources"><button>New Resource</button></Link></li>
          {/if}
          <!-- <Link to="SharedList"><button>Shared-List</button></Link> -->
          <li><Link to="Help"><button>Help</button></Link></li>
          <li><Link to="Account"><button>Account</button></Link></li>
          </ul>
        </nav>
    
    </div>
    </header>
  {/if}
</main>

<style>
  h2 {
    color: #ffffff;
    text-transform: uppercase;
    font-size: 3em;
    font-weight: 100;
    text-align: left;
  }

  .logo {
    float: left;
    height: 50%;
    padding-left: 2rem;
    padding-top: 2rem;
  }

  .ueberschrift {
    float: left;
    width: 100px;
    height: 50px;
    margin-top: 30px;
    padding-left: 2rem;
    margin: 0;
  }

  .box {
    height: 70px;
    min-width: 100%;
    padding-top: 10rem;
    padding-bottom: 1rem;
    /* padding-left: 5rem; */
    padding-right: 5rem;
   
     
  }


nav{
  background:radial-gradient(circle, #54789c 10%, #355779 100%);
  padding: 10px;
}

nav ul{
  list-style: none;
  margin: 0;
  padding: 0;
  display: flex;
  justify-content: space-around;
}

nav ul li  {
  display: inline-block;
}
  img {
    object-fit: cover;
    justify-content: left;
    align-items: left;
  }

  button {
    cursor: pointer;
    border-radius: 2em;
    color: #08243c;
    background: linear-gradient(to right, #b6c4d2, #ffffff);
    border: 0;
    padding-left: 10px;
    padding-right: 10px;
    padding-bottom: 10px;
    padding-top: 10px;
    margin-top: 10px;
    margin-bottom: 10px;
    margin-right: 10px;
    margin-left: 10px;

    font-size: 15px;
    box-shadow: 0 0 20px 1px rgba(0, 0, 0, 0.04);
  }

  button:hover {
    background-color: #74e1fc;
  }
</style>
