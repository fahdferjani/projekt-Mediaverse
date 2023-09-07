<!-- FavList.svelte -->
<script>
  import { onMount } from "svelte";
  import { createEventDispatcher } from "svelte";
  import FavContainer from "./FavContainer.svelte";
  import "@fortawesome/fontawesome-free/css/all.css";

  let token;
  let title = "";
  let favoriteLists = [];
  let favoriteItems = [];
  let types = [];
  let deleteErrorMessage = '';

  const dispatch = createEventDispatcher();

  onMount(async () => {
    // Retrieve the token from localStorage
    token = localStorage.getItem("token");

    // Fetch the user's favorite lists and items
    await fetchFavoriteLists();
    await fetchFavoriteItems();
  });

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
        favoriteLists = await response.json();
      } else {
        throw new Error("Failed to fetch favorite lists");
      }
    } catch (error) {
      console.error(error);
    }
  }

  async function createFavoriteList(event) {
    event.preventDefault();

    const newListData = {
      title: title,
    };

    try {
      const response = await fetch(
        "http://127.0.0.1:8000/favourite/favourite-lists/",
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            Authorization: `Token ${token}`,
          },
          body: JSON.stringify(newListData),
        }
      );

      if (response.ok) {
        console.log("Favorite list created successfully");
        title = ""; // Clear the form input

        // Fetch the updated favorite lists
        await fetchFavoriteLists();
      } else {
        throw new Error("Failed to create favorite list");
      }
    } catch (error) {
      console.error(error);
      alert("You can have only one Favorites list!");
    }
  }

  async function fetchFavoriteItems() {
    try {
      for (const favoriteList of favoriteLists) {
        const response = await fetch(
          `http://127.0.0.1:8000/favourite/favourite-items/?favourite_list=${favoriteList.id}`,
          {
            headers: {
              Authorization: `Token ${token}`,
            },
          }
        );

        if (response.ok) {
          const items = await response.json();

          for (const item of items) {
            const resource = await fetchResourceDetails(item.resource);
            item.resourceDetails = resource;
          }
          favoriteItems = items;
          
        } else {
          throw new Error("Failed to fetch favorite items");
        }
      }
    } catch (error) {
      console.error(error);
    }
  }

  async function fetchResourceDetails(resourceId) {
    try {
      const response = await fetch(
        `http://127.0.0.1:8000/resource/all-resources/${resourceId}/`,
        {
          headers: {
            Authorization: `Token ${token}`,
          },
        }
      );

      if (response.ok) {
        const resource = await response.json();
        return resource;
      } else {
        throw new Error("Failed to fetch resource details");
      }
    } catch (error) {
      console.error(error);
    }
  }


  async function deleteFavoriteList(listId) {
    try {
      const response = await fetch(`http://127.0.0.1:8000/favourite/favourite-lists/${listId}/`, {
        method: 'DELETE',
        headers: {
          Authorization: `Token ${token}`
        }
      });

      if (response.ok) {
        
        // Fetch the updated favorite lists
        await fetchFavoriteLists();
      } else {
        throw new Error('Failed to delete favorite list');
      }
    } catch (error) {
      console.error(error);
      deleteErrorMessage = 'Failed to delete favorite list';
    }
  }
  async function deleteFavoriteItem(itemId) {
    try {
      const response = await fetch(
        `http://127.0.0.1:8000/favourite/favourite-items/${itemId}/`,
        {
          method: 'DELETE',
          headers: {
            Authorization: `Token ${token}`
          }
        }
      );

      if (response.ok) {
       
        // Fetch the updated favorite items
        await fetchFavoriteItems();
      } else {
        throw new Error('Failed to delete favorite item');
      }
    } catch (error) {
      console.error(error);
      deleteErrorMessage = 'Failed to delete favorite item';
    }
  }

</script>

<main>
  <div id="container">
    <div id="wrapper">
      <div id="content">
        <h1>
          <strong
            ><i class="fas fa-star" /> Favourites List
            <i class="fas fa-star" /></strong
          >
        </h1>
        <div id="sec1">
          <p>
            Below you will find your personalised favourites list. If you have 
            not created one yet, make sure to give in the name of your list and 
            continue with adding some items.
          </p>
          <div id="FormC">
            {#if !Array.isArray(favoriteLists) || favoriteLists.length === 0}
              <form on:submit={createFavoriteList}>
                <label for="listName">Name of your Fav-list:</label>
                <div class="input-container">
                  <input
                    type="text"
                    id="listName"
                    bind:value={title}
                    required
                  />
                  <button type="submit">Create</button>
                </div>
              </form>
            {/if}
          </div>
        </div>

        <div id="Title">
          {#if Array.isArray(favoriteLists) && favoriteLists.length > 0}
            <ul>
              {#each favoriteLists as favoriteList}
                <h2 class="favorite-list-title">{favoriteList.title}</h2>
                <div id="TitleDelete">
                <button on:click={() => deleteFavoriteList(favoriteList.id)}>Reset your favourites</button>
              </div>
                {/each}
            </ul>
          {/if}
        </div>

        <!-- <h3>Your Favorite Items</h3> -->
        {#if !Array.isArray(favoriteItems) || favoriteItems.length === 0}
          <p>No favorite items found.</p>
        {/if}

        {#if Array.isArray(favoriteItems) && favoriteItems.length > 0}
          <div id="example3" class="container off-bottom">
            <div class="scrollbox">
              <ul class="list">
                {#each favoriteItems as favoriteItem}
                  <li class="item">
                    <div id="item-container">
                      {#if favoriteItem.resourceDetails}
                        <div class="picture">
                          <!-- svelte-ignore a11y-img-redundant-alt -->
                          <img src="./public/41AwrxBY38L.jpg" alt="photo" />
                        </div>
                        <div class="text">
                          <div id="head">
                            <p><strong>Title: </strong>{favoriteItem.resourceDetails.title}</p>
                            <p><strong>
                              Author: </strong>{favoriteItem.resourceDetails.author}</p>
                            
                            <p><strong> Year: </strong>{favoriteItem.resourceDetails.year} </p>
                          </div>
                          <div id="description">
                            <p><strong>
                              Description:</strong> {favoriteItem.resourceDetails
                                .description}
                            </p>
                            
                          </div>
                          <div id="info">
                            <p><strong>Link: </strong>{favoriteItem.resourceDetails.link}</p>
                            <p><strong>Code: </strong> {favoriteItem.resourceDetails.code}</p>
                            <p>
                              <strong>Categories:</strong> {#each favoriteItem.resourceDetails.categories as category}{category.name},
                              {/each}
                            </p>
                            <p>
                              <strong>Types: </strong>{#each favoriteItem.resourceDetails.types as type}{type.name},
                              {/each}
                            </p>
                            <p>
                              <strong>Is Available to Borrow:</strong> {favoriteItem
                                .resourceDetails.is_available_to_borrow
                                ? "Yes"
                                : "No"}
                            </p>
                            <p><strong>File:</strong> {favoriteItem.resourceDetails.file}</p>
            
                          </div>
                        </div>
                        
                        <button id="container_button" on:click={() => deleteFavoriteItem(favoriteItem.id)}>
                          Delete <i class="fas fa-trash" style="color:red; margin-left:5px"></i></button>
                      
                       
                      {/if}
                      


                    </div>
                  </li>
                {/each}
              </ul>
              <!-- if liste -->
            </div>
            <div class="shadow shadow-top" aria-hidden="true" />
            <div class="shadow shadow-bottom" aria-hidden="true" />
          </div>
        {/if}

        <div id="Info">
          <h3>Do you need help adding new Ressources to your list?</h3>
          <p>
            Simply search for the ressources you like in our search engine and
            click on the star icon to add it to your personalised list!
          </p>
        </div>

        <div id="footer">
          <img
            src="./public/login_logo.jpg"
            width="300"
            class="center"
            alt="MV-logo"
          />
        </div>
      </div>
    </div>
  </div>
</main>

<style lang="scss">
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
    align-items: center;
  }

  h1 {
    font-family: "Arial", sans-serif; /* Use any desired font family */
    text-transform: none;
    letter-spacing: 1px; /* Adjust the letter spacing as per the metro sign style */
  }

  h3 {
    font-family: "Arial", sans-serif; /* Use any desired font family */
    text-transform: none;
    letter-spacing: 1px; /* Adjust the letter spacing as per the metro sign style */
  }
  div {
    margin-bottom: 20px;
  }

  div#FormC label {
    font-family: "Arial", sans-serif; /* Use any desired font family */
    font-size: 10px; /* Adjust the font size as per the metro sign style */
    color: #ffffff; /* Adjust the font color as per the metro sign style */
    text-transform: none;
    letter-spacing: 1px; /* Adjust the letter spacing as per the metro sign style */
  }

  div#FormC input {
    color:#3d464f;
    background-color: #ffffff;
    width: auto;
  }

  div#FormC button {
    background-color: transparent;
    border: none;
    border-radius: 8px;
    color: white;
    font-size: 16px;
    padding: 10px 20px;
    text-align: center;
    text-decoration: none;
    display: inline-block;
    width: auto;
    transition-duration: 0.4s;
    cursor: pointer;
    box-shadow: 0px 2px 3px rgba(0, 0, 0, 0.5);
  }

  div#FormC button:hover {
    background-color: rgba(51, 51, 51, 0.6);
  }

  div#sec1 {
    display: flex;
    overflow-x: auto;
    width: auto;
    height: 200px;
    text-align: left;
    background-color: hsla(204, 31%, 73%, 0.7); /* Adjust the background color as per the metro sign style */
    border-radius: 15px; /* Adjust the border radius to create a curved style */
    align-items: center;
    justify-content: center;
   
  }

  div#Title {
    align-items: stretch;
    justify-content: center;
    overflow: auto;
  }

  div#Title h2 {
    font-family: "Arial", sans-serif; /* Use any desired font family */
    // font-size: 15px; /* Adjust the font size as per the metro sign style */
    color: #ffffff; /* Adjust the font color as per the metro sign style */
    text-transform: none;
    letter-spacing: 1px; /* Adjust the letter spacing as per the metro sign style */
  }

  div#sec1 p {
    font-family: "Arial", sans-serif; /* Use any desired font family */
    font-size: 15px; /* Adjust the font size as per the metro sign style */
    color: #ffffff; /* Adjust the font color as per the metro sign style */
    text-transform: none;
    letter-spacing: 1px; /* Adjust the letter spacing as per the metro sign style */
  }

  p {
    padding: 0 10px;
    line-height: 1.8;
  }

  div#container {
    width: 700px;
    margin: 0 auto;
  }

  div#footer {
    clear: both;
    width: 100%;
  }

  div#Info {
    margin-left: 30px;
    font-family: "Arial", sans-serif; /* Use any desired font family */
    font-size: 15px; /* Adjust the font size as per the metro sign style */
    color: #374046; /* Adjust the font color as per the metro sign style */
    text-transform: none;
    letter-spacing: 1px; /* Adjust the letter spacing as per the metro sign style */
  }

  /* scrollbox style */

  #example3 {
    overflow: hidden;
    position: relative;

    .scrollbox {
      height: 100%;
      overflow: auto;
    }
    .shadow {
      bottom: 0;
      left: 0;
      pointer-events: none;
      position: absolute;
      right: 0;
      top: 0;
      transition: all 0.2s ease-out;
    }
    .shadow off-top {
      .shadow-top {
        box-shadow: 0 1em 1em -1em black inset;
      }
    }
    .shadow off-bottom {
      .shadow-bottom {
        box-shadow: 0 -1em 1em -1em black inset;
      }
    }
  }

  .container {
    background-color: white;
    border: solid 0.5em rgb(137, 136, 136);
    border-radius: 0.5em;
    box-sizing: border-box;
    flex: 0 0 30%;
    height: 500px;
    margin: 0.5em;
    overflow: auto;
  }

  .list {
    list-style: none;
    margin: 0;
    padding: 0;
    height: 100%;
  }

  .item {
    background-color: lightgray;
    margin-top: 2%;
    padding: 0.3%;
    height: auto;
  }

  @keyframes flash {
    0%,
    100% {
      opacity: 1;
    }
    50% {
      opacity: 0.2;
    }
  }

  div#item-container {
    width: auto;
    height:fit-content;
    margin: 0 auto;
    padding: 20px;
    background-color: rgba(255, 255, 255, 0.8);
    border-radius: 10px;
    box-shadow: 0 2px 6px rgba(0, 0, 0, 0.15);
    display: flex;
    overflow: scroll;
  }
  .picture img {
    width: 200px;
    height: 250px;
    object-fit: cover;
    border-radius: 10px;
  }
  .text {
    text-align: left;
    margin-left: 5px;
    font-family: "Arial", sans-serif; /* Use any desired font family */
    font-size: 15px; /* Adjust the font size as per the metro sign style */
    color: #1b3545; /* Adjust the font color as per the metro sign style */
    text-transform: none;
    letter-spacing: 1px; /* Adjust the letter spacing as per the metro sign style */
  }

  #container_button {
    background-color: transparent;
    border: none;
    border-radius: 4px;
    color: rgb(16, 11, 11);
    font-size: 16px;
    padding: 5px 10px;
    text-align: center;
    text-decoration: none;
    display: inline-block;
    height: 10%;
    transition-duration: 0.4s;
    cursor: pointer;
    box-shadow: 0px 2px 3px rgba(0, 0, 0, 0.5);
    margin-top: 35%;
  }

  #TitleDelete button {
    background-color: transparent;
    border: none;
    border-radius: 4px;
    color: rgb(52, 49, 49);
    font-size: 16px;
    padding: 5px 10px;
    text-align: center;
    text-decoration: none;
    display: inline-block;
    height: 10%;
    width:auto;
    transition-duration: 0.4s;
    cursor: pointer;
    box-shadow: 0px 2px 3px rgba(0, 0, 0, 0.5);
  }


</style>