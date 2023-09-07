<!-- BorrowedResourcesList.svelte -->
<script>
  import { onMount } from "svelte";
  let token;
  let borrowedResources = [];
  let previousBorrowedResources = [];

  onMount(async () => {
    // Retrieve the token from localStorage
    token = localStorage.getItem("token");

    // Fetch the user's currently borrowed resources
    await fetchCurrentBorrowedResources();
    // Fetch the user's previously borrowed resources
    await fetchPreviousBorrowedResources();
  });

  async function fetchCurrentBorrowedResources() {
    try {
      const response = await fetch("http://127.0.0.1:8000/borrow/transactions/current/", {
        headers: {
          Authorization: `Token ${token}`
        }
      });

      if (response.ok) {
        const items = await response.json();

        for (const item of items) {
          const resource = await fetchResourceDetails(item.resource);
          item.resourceDetails = resource;
        }
        borrowedResources = items;
      } else {
        throw new Error("Failed to fetch currently borrowed resources");
      }
    } catch (error) {
      console.error(error);
    }
  }

  async function fetchPreviousBorrowedResources() {
    try {
      const response = await fetch("http://127.0.0.1:8000/borrow/transactions/previous/", {
        headers: {
          Authorization: `Token ${token}`
        }
      });

      if (response.ok) {
        const items = await response.json();

        for (const item of items) {
          const resource = await fetchResourceDetails(item.resource);
          item.resourceDetails = resource;
        }
        previousBorrowedResources = items;
      } else {
        throw new Error("Failed to fetch previously borrowed resources");
      }
    } catch (error) {
      console.error(error);
    }
  }

  async function fetchResourceDetails(resourceId) {
    try {
      const response = await fetch(`http://127.0.0.1:8000/resource/all-resources/${resourceId}/`, {
        headers: {
          Authorization: `Token ${token}`
        }
      });

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

 async function extendResource(transactionId) {
  try {
    const response = await fetch(`http://127.0.0.1:8000/borrow/transactions/${transactionId}/extend/`, {
      method: "POST",
      headers: {
        Authorization: `Token ${token}`,
        "Content-Type": "application/json",
      },
    });

    if (response.ok) {
      await fetchCurrentBorrowedResources();
      alert("Borrowing duration successfully extended!");
    } else {
      throw new Error("Failed to extend resource borrowing period");
    }
  } catch (error) {
    console.error(error);
  }
}

async function returnResource(transactionId) {
  try {
    const response = await fetch(`http://127.0.0.1:8000/borrow/transactions/${transactionId}/return/`, {
      method: "POST",
      headers: {
        Authorization: `Token ${token}`,
        "Content-Type": "application/json",
      },
    });

    if (response.ok) {
      await fetchCurrentBorrowedResources();
      await fetchPreviousBorrowedResources();
      alert("Resource successfully returned!");
    } else {
      throw new Error("Failed to return resource");
    }
  } catch (error) {
    console.error(error);
  }
}

</script>

<main>
<div id="wrapper1">
  <h1>List of Currently Borrowed Resources</h1>
  <div id="container1">
    {#if Array.isArray(borrowedResources) && borrowedResources.length > 0}
    <div id="example3" class="container off-bottom">
      <div class="scrollbox">
        <ul class="list">
        {#each borrowedResources as resource}
          {#if resource.resourceDetails}
          <li class="item">
            <div id="item-container">
            <div class="picture">
              <!-- svelte-ignore a11y-img-redundant-alt -->
              <img src="./public/41AwrxBY38L.jpg" alt="photo" />
            </div>
            <div class="text">
              <div id="head">
                <strong>{resource.resourceDetails.title}</strong> by {resource.resourceDetails.author}
                <p><strong>Description:</strong> {resource.resourceDetails.description}</p>
                <p><strong>Returned:</strong> {resource.returned}</p>
                <p><strong>Number of Extends:</strong> {resource.number_of_extends}</p>
                <p><strong>Borrowed on:</strong> {resource.borrow_date}</p>
                <p><strong>Due date:</strong> {resource.due_date}</p>

                <div class="buttons">
                <button on:click={() => extendResource(resource.id)}>Extend</button>
                <button on:click={() => returnResource(resource.id)}>Return</button>
              </div>
              </div>
            </div>
          </div>
          </li>
        {/if}
      {/each}
    </ul>
    <div class="shadow shadow-top" aria-hidden="true" />
            <div class="shadow shadow-bottom" aria-hidden="true" />
    </div>
  </div>
  {:else}
    <p>No currently borrowed resources found.</p>
  {/if}
            
</div>

<div id="wrapper2">
  <h1>List of Previously Borrowed Resources</h1>
<div id="container2">
  
  {#if Array.isArray(previousBorrowedResources) && previousBorrowedResources.length > 0}
    <div id="example3" class="container off-bottom">
      <div class="scrollbox">
        <ul class="list">
          {#each previousBorrowedResources as resource}
            {#if resource.resourceDetails}
              <li class="item">
                <div id="item-container">
                  <!-- svelte-ignore a11y-img-redundant-alt -->
                <div class="picture">
                  <img src="./public/41AwrxBY38L.jpg" alt="photo" />
                </div>
                <div class="text">
                  <div id="head">
                    <strong>{resource.resourceDetails.title}</strong> by {resource.resourceDetails.author}
                    <p><strong>Description:</strong> {resource.resourceDetails.description}</p>
                    <p><strong>Returned:</strong> {resource.returned}</p>
                    <p><strong>Number of Extends:</strong> {resource.number_of_extends}</p>
                    <p><strong>Borrowed on:</strong> {resource.borrow_date}</p>
                    <p><strong>Due date:</strong> {resource.due_date}</p>
                  </div>
                </div>  
              </div>
              </li>
            {/if}
          {/each}
        </ul>
      </div>
    </div>
  {:else}
    <p>No previously borrowed resources found.</p>
  {/if}
</div>
</div>
</div>
</main>

<style lang="scss">
main {
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
  

ul {
  list-style: none;
  padding: 0;
  padding: 20px;
  background-color: rgba(255, 255, 255, 0.8);
  border-bottom-left-radius: 10px;
  border-bottom-right-radius: 10px;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.15);
}

li {
  margin-bottom: 10px;
  border: 1px solid #ddd;
  padding: 10px;
  border-radius: 5px;
}


div#wrapper1 {
  width: 1200px;
  padding: 20px;
  border-bottom-left-radius: 10px;
  border-bottom-right-radius: 10px;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.15);
  align-items: center;
}

div#wrapper1 {
  align-items: center;
  display:grid;
  margin-top: 10px;
  
}

div#wrapper2 {
  align-items: center;
  display:grid;
  margin-top: 80px;
}

div#container1 {
 width: 80%;
 height: cover;
 position:center;
 margin-top: 20px;
 margin-left: 125px;
}

div#container2 {
  width: 80%;
  height: cover;
  margin: 100px;
  margin-top: 20px;
  margin-left: 125px;
  


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

</style>