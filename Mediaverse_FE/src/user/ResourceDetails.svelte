<!-- Homepage.svelte -->
<script>
    import { onMount } from 'svelte';
    import { createEventDispatcher } from 'svelte';
    import { Router, Route} from 'svelte-navigator';
    import { sharedValue1, sharedValue2, sharedValue3, sharedValue4, sharedValue5, sharedValue6, sharedValue7, sharedValue8, sharedValue9, sharedValue10 } from '../store.js';



    let token;
    let username;
    let email;
    let isMediathekar;
    let searchTitle = '';
    let searchYear = '';
    let searchAuthor = '';
    let resources = [];
    let categories = [];
    let selectedCategories = [];
    let types = [];
    let selectedTypes = [];
    let buttonText = 'add to Fav-List';
  
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
          // Extract user information from the response
          username = data.username;
          email = data.email;
          isMediathekar = data.is_mediathekar;
        } else {
          throw new Error('Failed to fetch user information');
        }
      } catch (error) {
        // Handle error
        console.error(error);
      }
    });
    
  
    async function fetchResources() {
        try {
          let url = 'http://127.0.0.1:8000/resource/all-resources/';
    
          // Add search query parameter if searchTitle is provided
          if (searchTitle) {
            url += `?title=${encodeURIComponent(searchTitle)}`;
          }
    
          // Add author query parameter if searchAuthor is provided
          if (searchAuthor) {
            url += `${searchTitle || searchYear ? '&' : '?'}author=${encodeURIComponent(searchAuthor)}`;
          }
    
          // Add year query parameter if searchYear is provided
          if (searchYear) {
            url += `${searchTitle || searchAuthor ? '&' : '?'}year=${encodeURIComponent(searchYear)}`;
          }
    
          // Add categories query parameter if selectedCategories is not empty
          if (selectedCategories.length > 0) {
            const categoriesQuery = selectedCategories.join(',');
            url += `${searchTitle || searchAuthor || searchYear ? '&' : '?'}categories=${encodeURIComponent(categoriesQuery)}`;
          }
    
          // Add types query parameter if selectedTypes is not empty
          if (selectedTypes.length > 0) {
            const typesQuery = selectedTypes.join(',');
            url += `${url.includes('?') ? '&' : '?'}types=${encodeURIComponent(typesQuery)}`;
          }
    
          const response = await fetch(url, {
            headers: {
              Authorization: `Token ${token}`
            }
          });
    
          if (response.ok) {
            resources = await response.json();
          } else {
            throw new Error('Failed to fetch resources');
          }
        } catch (error) {
          console.error(error);
        }
      }
  
  
  
      async function fetchCategories() {
        try {
          const response = await fetch('http://127.0.0.1:8000/resource/all-categories/', {
            headers: {
              Authorization: `Token ${token}`
            }
          });
    
          if (response.ok) {
            categories = await response.json();
          } else {
            throw new Error('Failed to fetch categories');
          }
        } catch (error) {
          console.error(error);
        }
      }
  
  
  
      async function fetchTypes() {
        try {
          const response = await fetch('http://127.0.0.1:8000/resource/all-types/', {
            headers: {
              Authorization: `Token ${token}`
            }
          });
    
          if (response.ok) {
            types = await response.json();
          } else {
            throw new Error('Failed to fetch types');
          }
        } catch (error) {
          console.error(error);
        }
      }

  async function addToFavList(resourceId, share) {
    try {
      const response = await fetch(
        "http://127.0.0.1:8000/favourite/favourite-items/",
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            Authorization: `Token ${token}`,
          },
          body: JSON.stringify({
            resource: resourceId,
            share: share,
          }),
        }
      );

      if (response.ok) {
        console.log("Resource added to Fav-List");
        // Update the button text or perform any other necessary actions

        // Fetch the updated favorite lists
        await fetchFavoriteLists();
      } else {
        throw new Error("Failed to add resource to Fav-List");
      }
    } catch (error) {
      console.error(error);
    }
  }

  async function fetchFavoriteLists() {
    try {
      const response = await fetch(
        "http://127.0.0.1:8000/favourite/favourite-lists/",
        {
          headers: {
            Authorization: `Token ${token}`,
          },
        }
      );

      if (response.ok) {
        // Fetch the updated favorite lists
        const favoriteLists = await response.json();
        dispatch("updateFavoriteLists", favoriteLists);
      } else {
        throw new Error("Failed to fetch favorite lists");
      }
    } catch (error) {
      console.error(error);
    }
  }

  function addClick(resourceId, share) {
    addToFavList(resourceId, share);
  }

  function handleCategorySelection(event) {
    const categoryId = Number(event.target.value);
    const isChecked = event.target.checked;

    // Update the selectedCategories array
    if (isChecked) {
      selectedCategories = [...selectedCategories, categoryId];
    } else {
      selectedCategories = selectedCategories.filter((id) => id !== categoryId);
    }
  }

  function handleTypeSelection(event) {
    const typeId = Number(event.target.value);
    const isChecked = event.target.checked;

    // Update the selectedTypes array
    if (isChecked) {
      selectedTypes = [...selectedTypes, typeId];
    } else {
      selectedTypes = selectedTypes.filter((id) => id !== typeId);
    }
  }

  async function handleClick(resourceId) {
    try {
      const response = await fetch(
        `http://127.0.0.1:8000/borrow/resources/${resourceId}/borrow/`,
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            Authorization: `Token ${token}`,
          },
        }
      );

      if (response.ok) {
        // Borrow request successful
        console.log("Resource borrowed successfully");
        alert("Resource borrowed successfully");
      } else {
        const errorData = await response.json();
        throw new Error(`Failed to borrow resource: ${errorData.detail}`);
      }
    } catch (error) {
      console.error("Error: Failed to borrow resource at handleClick", error);
    }
  }

  onMount(fetchCategories);
  onMount(fetchTypes);
  
</script>
  
<main>
  {#if token}
    <div id="wrapper">      
      <h1>{$sharedValue2}</h1>

      <div id="container">
      <div class="picture">
        <img src="./public/41AwrxBY38L.jpg" alt="photo" />
      </div> 
      
      <div id="box">
        
        <div id="author_year">
          <h4>Author: {$sharedValue3}</h4>
          <h4>Year: {$sharedValue4}</h4>
        </div>

        <div id="description"> 
          <p>{$sharedValue10 ? $sharedValue10 : "No Description"}</p> 
        </div>

        <div id="infos">
          <p>Link: {$sharedValue5  ? $sharedValue5 : "No Link"}</p>
          <p>File: {$sharedValue9  ? $sharedValue9 : "No File"}</p>
          <div id="order">
            <p> Is Available to Borrow: {$sharedValue8  ? "Yes" : "No"}</p>
            <p>Id: {$sharedValue1}</p>
            <button on:click={() => handleClick($sharedValue1)}>Borrow</button>       
            <button on:click={() => addClick($sharedValue1)}
              >Add To Favourites<i class="fas fa-star" style="color: gold; margin-left: 2px;" /></button
            >
          </div>
        </div>
      </div>
    </div>
    </div> 
   

  {:else}
    <p>Please login to access this page.</p>
    <button on:click={() => dispatch('showLogin', {})}>Login</button>
  {/if}
</main>
  
<style>
  main {
    margin: 0;
    padding: 0;
    height: cover;
    width: cover;
    font-family: "Helvetica", sans-serif;
    line-height: 1.2em;
    background: radial-gradient(circle, #b6c4d2 10%, #355779 100%);
    justify-content: center;
    color: #dce4ec;
    line-height: 1.5;
    border-radius: 15px; /* Adjust the border radius to create a curved style */
    display: flex;
    text-align: left;
  }


  h1, h4 {
    font-family: "Arial", sans-serif; /* Use any desired font family */
    text-transform: none;
    letter-spacing: 1px; /* Adjust the letter spacing as per the metro sign style */
    text-align: center;
  }

  p {
      text-align: center;
      color: #374046;
  }

  div#wrapper {
    margin-top: 10px;
    width: 1100px;
    height: cover;
  }

  #wrapper h1 {
    text-align: center;
  }

  #container {
    display: grid;
    grid-template-columns: 300px 700px;
  }

  #box {
    width: 700px;
    height: cover;
    text-align: left;
    margin-left: 30px;
    margin-top: 30px;
  }

  .picture img {
    width: 300px;
    height: 375px;
    margin-top: 30px;
    margin-right: 20px;
    object-fit: cover;
    border-radius: 10px;
  }

  div.picture {
    text-align: left;
    margin-top: 20px;
  }

    div#author_year {
      display: grid;
      grid-template-columns: auto auto;
      width: 600px;
    }

    #description {
      display: flex;
      overflow-x: auto;
      width: 600px;
      height: cover;
      margin-top: 0;
      margin-bottom: 30px;
      margin-left: 30px;
      margin-right: 30px;
      background-color: #8ba2b1; 
      border-radius: 15px; 
      align-items: center;
      justify-content: center;
      padding: 20px;
    }

    div#infos {
      
      width: 600px;
      height: cover;
      margin-top: 20px;
      margin-bottom: 50px;
      margin-left: 100px;
    }

    div#order {
      display: grid;
      grid-template-columns: auto auto;
    }

    #infos p {
      text-align: left;

    }



  </style>