<!-- Homepage.svelte -->
<script>
  import { onMount } from "svelte";
  import { createEventDispatcher } from "svelte";
  import { Router, Route, Link } from "svelte-navigator";
  import { sharedValue1, sharedValue2, sharedValue3, sharedValue4, sharedValue5, sharedValue6, sharedValue7, sharedValue8, sharedValue9, sharedValue10 } from './store.js';
  import Header from "./user/Header.svelte";
  import FavList from "./user/FavourtiesList/FavList.svelte";
  import ResourcesList from "./user/ResourcesList.svelte";
  import ResourceDetails from "./user/ResourceDetails.svelte";
  import Bibliothekar from "./Bibliothekar.svelte";
  import Help from "./user/Help.svelte";
  import Account from "./user/Account.svelte";
  import Login from "./Login.svelte";
  import QRCode from "./QRCode.svelte";
  //import Webcam from "./Webcam.svelte";

  let token;
  let username;
  let email;
  let isMediathekar;
  let searchTitle = "";
  let searchYear = "";
  let searchAuthor = "";
  let resources = [];
  let categories = [];
  let selectedCategories = [];
  let types = [];
  let selectedTypes = [];
  let buttonText = "add to Fav-List";

  const dispatch = createEventDispatcher();

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

  async function fetchResources() {
    try {
      let url = "http://127.0.0.1:8000/resource/all-resources/";

      // Add search query parameter if searchTitle is provided
      if (searchTitle) {
        url += `?title=${encodeURIComponent(searchTitle)}`;
      }

      // Add author query parameter if searchAuthor is provided
      if (searchAuthor) {
        url += `${
          searchTitle || searchYear ? "&" : "?"
        }author=${encodeURIComponent(searchAuthor)}`;
      }

      // Add year query parameter if searchYear is provided
      if (searchYear) {
        url += `${
          searchTitle || searchAuthor ? "&" : "?"
        }year=${encodeURIComponent(searchYear)}`;
      }

      // Add categories query parameter if selectedCategories is not empty
      if (selectedCategories.length > 0) {
        const categoriesQuery = selectedCategories.join(",");
        url += `${
          searchTitle || searchAuthor || searchYear ? "&" : "?"
        }categories=${encodeURIComponent(categoriesQuery)}`;
      }

      // Add types query parameter if selectedTypes is not empty
      if (selectedTypes.length > 0) {
        const typesQuery = selectedTypes.join(",");
        url += `${url.includes("?") ? "&" : "?"}types=${encodeURIComponent(
          typesQuery
        )}`;
      }

      const response = await fetch(url, {
        headers: {
          Authorization: `Token ${token}`,
        },
      });

      if (response.ok) {
        resources = await response.json();
      } else {
        throw new Error("Failed to fetch resources");
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

  async function fetchCategories() {
    try {
      const response = await fetch(
        "http://127.0.0.1:8000/resource/all-categories/",
        {
          headers: {
            Authorization: `Token ${token}`,
          },
        }
      );

      if (response.ok) {
        categories = await response.json();
      } else {
        throw new Error("Failed to fetch categories");
      }
    } catch (error) {
      console.error(error);
    }
  }

  async function fetchTypes() {
    try {
      const response = await fetch(
        "http://127.0.0.1:8000/resource/all-types/",
        {
          headers: {
            Authorization: `Token ${token}`,
          },
        }
      );

      if (response.ok) {
        types = await response.json();
      } else {
        throw new Error("Failed to fetch types");
      }
    } catch (error) {
      console.error(error);
    }
  }

  async function handleSearch(event) {
    event.preventDefault();
    await fetchResources();
  }

  function logout() {
    // Clear the token from localStorage
    localStorage.removeItem("token");

    // Dispatch event to switch to the Login component
    dispatch("showLogin", {});
  }

  function qrCode() {
    dispatch("showqr", {});
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

  /**
     * @param {string} id
     * @param {string} [title]
     * @param {string} [author]
     * @param {string} [Year]
     * @param {string} [link]
     * @param {string} [is_available_to_borrow]
     * @param {string} [file]
     * @param {string} [description]
     */
  function updateValue(id, title, author, Year, link, is_available_to_borrow, file, description) {
    sharedValue1.set(id);
    sharedValue2.set(title);
    sharedValue3.set(author);
    sharedValue4.set(Year);
    sharedValue5.set(link);

    sharedValue8.set(is_available_to_borrow);
    sharedValue9.set(file);
    sharedValue10.set(description);
  }

</script>

<main>
  {#if token}
    <div class="logout">
      <button on:click={logout}>Logout</button>
    </div>

    <Router>
      <Header />
      <Route path="/">
        <body>
          <div id="box">
            <div id="SearchEngineContainer">
              <h1>Search Resources</h1>

              <form on:submit={handleSearch}>
                <div id="search-boxes">
                  <input
                    type="text"
                    bind:value={searchTitle}
                    placeholder="Enter resource title"
                  />
                  <input
                    type="text"
                    bind:value={searchAuthor}
                    placeholder="Enter author name"
                  />
                  <input
                    type="text"
                    bind:value={searchYear}
                    placeholder="Enter year"
                  />
                </div>

                <button id="search-button" type="submit">Search</button>
                <Link to="QRCode"><button id="qr-search-button" >
                  QR <i class="fa fa-qrcode" style="padding-left: 5px;" />
                </button></Link>
              </form>

              <!-- <div class="dropdown">
                <button class="dropbtn">Categories</button>
                <div class="dropdown-content">
                  <li>item1</li>
                  <li>item2</li>
                  <li>item3</li>
                  <li>item4</li>
                </div>
              </div> -->

              <div class="dropdown">
                <!-- <div id="cat"> -->
                <button class="dropbtn">Categories</button>
                <div class="dropdown-content">
                  {#if categories.length > 0}
                    {#each categories as category}
                      <!-- <label>
                      <h3>Categories</h3> -->

                      <input
                        type="checkbox"
                        value={category.id}
                        on:change={handleCategorySelection}
                      />
                      {category.name}

                      <!-- </label> -->
                    {/each}
                  {/if}
                </div>
              </div>

              <div class="dropdown-2">
                <button class="dropbtn-2">Types</button>
                <div class="dropdown-content-2">
                  {#if types.length > 0}
                    {#each types as type}
                      <!-- <label> -->
                      <!-- <h3>Types</h3> -->
                      <input
                        type="checkbox"
                        value={type.id}
                        on:change={handleTypeSelection}
                      />
                      {type.name}
                      <!-- </label> -->
                    {/each}
                  {/if}
                </div>
              </div>
            </div>

            <div id="wrapper">
              {#if resources.length > 0}
                <!-- <h2>Search Results</h2> -->
                <div id="example3" class="container off-bottom">
                  <div class="scrollbox">
                    <ul class="list">
                      {#each resources as resource}
                        <li class="item">
                          <div class="picture">
                            <!-- svelte-ignore a11y-img-redundant-alt -->
                            <img src="./public/41AwrxBY38L.jpg" alt="photo" />
                          </div>
                          <div class="text">
                            <div id="head">
                              <p><strong>Title:</strong>{resource.title}</p>
                              <p><strong>Author:</strong>{resource.author}</p>
                              <p><strong>Year:</strong>{resource.year}</p>
                            </div>
                            <div id="info">
                              <p><strong>
                                Categories: </strong>{#each resource.categories as category}{category.name},
                                {/each}
                              </p>
                              <p><strong>
                                Types: </strong>{#each resource.types as type}{type.name},
                                {/each}
                              </p>
                              <p><strong>
                                Barrowable: </strong>{resource.is_available_to_borrow
                                  ? "Yes"
                                  : "No"}
                              </p>
                              {#if resource.file}
                                <p><strong>File: </strong>{resource.file}</p>
                              {/if}
                            </div>
                          </div>

                          
                          <div id="description">

                            <Link to="ResourceDetails"><button 
                              on:click={() => updateValue(resource.id, resource.title, resource.author, resource.year, resource.link, resource.is_available_to_borrow, resource.file, resource.description, )}>
                              View Details</button></Link>
                            <br />
                            <br />
                            <button on:click={() => handleClick(resource.id)}
                              >Borrow</button>
                            <br />
                            <br />
                            <button on:click={() => addClick(resource.id)}
                              >Add To Favourites<i class="fas fa-star" style="color: gold; margin-left: 2px;" /></button>
                          </div>

                        </li>
                      {/each}
                    </ul>
                  </div>
                  <div class="shadow shadow-top" aria-hidden="true" />
                  <div class="shadow shadow-bottom" aria-hidden="true" />
                </div>
              {:else}
                <p>No resources found.</p>
              {/if}
            </div>
          </div>
        </body>
      </Route>
      <Route path="FavList" component={FavList} />
      <Route path="ResourcesList" component={ResourcesList} />
      <Route path="CreateResources" component={Bibliothekar} />
      <Route path="Help" component={Help} />
      <Route path="Account" component={Account} />
      <Route path="ResourceDetails" component={ResourceDetails} />
      <Route path="QRCode" component={QRCode} />


    </Router>
  {:else}
    <p>Please login to access this page.</p>
    <button on:click={() => dispatch("showLogin", {})}>Login</button>
  {/if}
</main>

<style lang="scss">
  body {
    margin: 0;
    padding: 0;
    min-height: 700px;

    min-width: 100%;
    font-family: "Helvetica", sans-serif;
    line-height: 1.2em;
    background: radial-gradient(circle, #b6c4d2 10%, #355779 100%);
    justify-content: center;
    color: #dce4ec;
    line-height: 1.5;
    border-radius: 15px;
    display: flex;
    align-items: center;
  }

  .logout {
    float: right;
    padding: 1rem;
    margin: auto;
  }

  h1 {
    margin-bottom: 60px;
    color: #08243c;
    padding-top: 3rem;
    size: 3rem;
  }

  // p {
  //   text-align: left;
  // }

  input {
    width: 190px;
    height: 25px;
  }

  // label {
  //   display: grid;
  //   grid-template-columns: 100px 50px 100px;
  //   justify-items: center;
  //   align-items: center;
  //   justify-content: end;
  //   align-content: center;
  // }

  ul {
    margin: 0;
    padding: 0;
    list-style-type: none;
  }

  li {
    display: grid;
    grid-template-columns: auto auto auto auto;
  }

  // li p {
  //   position: static;
  //   color:#000000;
  // }

  #box {
    min-width: 70%;
  }
  #wrapper {
    min-width: auto;
  }

  #search-boxes {
    display: flex;
    flex-wrap: wrap;
    align-items: center;
    margin-bottom: 20px;
    margin-top: 20px;
  }

  #search-boxes input {
    margin-bottom: 3px;
    margin-right: 10px;
    padding: 10px;
    border: 1px solid #ccc;
    background-color: rgba(250, 247, 247, 0.5);
    border-radius: 5px;
    width: 100%;
    box-sizing: border-box;
    font-size: 15px;
    color: #000000;
  }

  div#SearchEngineContainer {
    margin: 0 auto;
    padding: 20px;
    background-color: rgba(250, 247, 247, 0.5);
    border-top-left-radius: 10px;
    border-top-right-radius: 10px;
  }

  #search-button {
    width: 80px;
    padding: 10px;
    font-size: 14px;
    background-color: #007aff;
    border: none;
    border-radius: 20px;
    color: white;
    cursor: pointer;
    box-shadow: 0px 2px 3px rgba(0, 0, 0, 0.5);
  }

  .dropbtn {
    margin-top: 20px;
    width: 100px;
    padding: 10px;
    font-size: 14px;
    background-color: #525353;
    border: none;
    border-radius: 20px;
    color: white;
    cursor: pointer;
    box-shadow: 0px 2px 3px rgba(0, 0, 0, 0.5);
  }

  #search-button:hover {
    background-color: rgba(51, 51, 51, 0.6);
  }

  #qr-search-button {
    width: 80px;
    padding: 10px;
    font-size: 14px;
    background-color: #007aff;
    border: none;
    border-radius: 20px;
    color: white;
    cursor: pointer;
    box-shadow: 0px 2px 3px rgba(0, 0, 0, 0.5);
  }

  #qr-search-button:hover {
    background-color: rgba(51, 51, 51, 0.6);
  }

  .dropdown {
    position: relative;
    display: inline-block;
  }

  .dropdown-content {
    display: none;
    position: absolute;
    background-color: #f9f9f9;
    color: #08243c;
    min-width: 50px;
    box-shadow: 0px 8px 16px 0px rgba(0, 0, 0, 0.2);
    padding: 12px 16px;
    z-index: 1;
  }

  .dropdown-2 {
    position: relative;
    display: inline-block;
  }

  .dropdown-content-2 {
    display: none;
    position: absolute;
    background-color: #f9f9f9;
    color: #08243c;
    min-width: 50px;
    box-shadow: 0px 8px 16px 0px rgba(0, 0, 0, 0.2);
    padding: 12px 16px;
    z-index: 1;
  }

  .dropbtn-2 {
    margin-top: 20px;
    width: 100px;
    padding: 10px;
    font-size: 14px;
    background-color: #525353;
    border: none;
    border-radius: 20px;
    color: white;
    cursor: pointer;
    box-shadow: 0px 2px 3px rgba(0, 0, 0, 0.5);
  }

  .dropdown:hover .dropdown-content {
    display: block;
  }

  .dropdown:hover .dropbtn {
    background-color: #6f7982;
  }

  .dropdown-2:hover .dropdown-content-2 {
    display: block;
  }

  .dropdown-2:hover .dropbtn-2 {
    background-color: #6f7982;
  }

  /* Styles for the results box */
  div#wrapper {
    width: auto;
    margin: 0 auto;
    padding: 20px;
    background-color: rgba(255, 255, 255, 0.8);
    border-bottom-left-radius: 10px;
    border-bottom-right-radius: 10px;
    box-shadow: 0 2px 6px rgba(0, 0, 0, 0.15);
  }
  .picture img {
    width: 200px;
    height: 250px;
    margin-right: 20px;
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
    border: solid 0.5em rgb(123, 123, 123);
    border-radius: 0.5em;
    box-sizing: border-box;
    flex: 0 0 30%;
    height: 500px;
    width: auto;
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
    background-color: rgb(220, 223, 231);
    margin-top: 2%;
    padding: 0.3%;
    height: auto;
  }


  .item button {
    margin-top:10%;
    position:relative;
    width: 20vh;
    text-align: center;
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
</style>