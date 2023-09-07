<!-- Bibliothekar.svelte -->
<script>
  import { onMount } from 'svelte';
  import { createEventDispatcher } from 'svelte';

  let token;
  let title = '';
  let author = '';
  let year = '';
  let link = '';
  let code = '';
  let categories = '';
  let types = '';
  let description = '';
  let file = null;
  let createdResources = [];

  let existingCategories = [];
  let existingTypes = [];
  let showCategoryOptions = false;
  let showTypeOptions = false;

  const dispatch = createEventDispatcher();

  onMount(async () => {
    // Retrieve the token from localStorage
    token = localStorage.getItem('token');
    await fetchExistingCategoriesAndTypes(); // Fetch existing categories and types
    await fetchCreatedResources(); // Fetch created resources
  });

  async function fetchExistingCategoriesAndTypes() {
    try {
      // Perform API calls to fetch existing categories and types
      const categoriesResponse = await fetch('http://127.0.0.1:8000/resource/all-categories/', {
        headers: {
          Authorization: `Token ${token}`,
        },
      });
      const typesResponse = await fetch('http://127.0.0.1:8000/resource/all-types/', {
        headers: {
          Authorization: `Token ${token}`,
        },
      });

      if (categoriesResponse.ok && typesResponse.ok) {
        existingCategories = await categoriesResponse.json();
        existingTypes = await typesResponse.json();
      } else {
        console.error('Failed to fetch existing categories and types');
      }
    } catch (error) {
      console.error('Failed to fetch existing categories and types', error);
    }
  }

  function toggleCategoryOptions() {
    showCategoryOptions = !showCategoryOptions;
  }

  function toggleTypeOptions() {
    showTypeOptions = !showTypeOptions;
  }

  async function createResource() {
    const resourceData = {
      title,
      author,
      year,
      link,
      code,
      categories: categories.split(',').map((name) => ({ name: name.trim() })),
      types: types.split(',').map((name) => ({ name: name.trim() })),
      description,
    };

    try {
      const response = await fetch('http://127.0.0.1:8000/resource/resources/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          Authorization: `Token ${token}`,
        },
        body: JSON.stringify(resourceData),
      });

      if (response.ok) {
        console.log('Resource created successfully');
        // Clear the form inputs
        title = '';
        author = '';
        year = '';
        link = '';
        code = '';
        categories = '';
        types = '';
        description = '';

        // Fetch the updated resources list
        await fetchCreatedResources();

        // Dispatch event to notify the parent component
        dispatch('resourceCreated', {});

        // Dispatch event to switch to the Homepage component
        dispatch('showHeader', {});
      } else {
        console.error('Failed to create resource');
      }
    } catch (error) {
      console.error(error);
    }
  }

  async function fetchCreatedResources() {
    try {
      const response = await fetch('http://127.0.0.1:8000/resource/resources/', {
        headers: {
          Authorization: `Token ${token}`,
        },
      });

      if (response.ok) {
        createdResources = await response.json();
      } else {
        throw new Error('Failed to fetch created resources');
      }
    } catch (error) {
      console.error(error);
    }
  }

  async function uploadFile(resourceId, file, title) {
    try {
      const formData = new FormData();
      formData.append('file', file);
      formData.append('title', title);

      const response = await fetch(`http://127.0.0.1:8000/resource/resources/${resourceId}/`, {
        method: 'PATCH',
        headers: {
          Authorization: `Token ${token}`
        },
        body: formData
      });

      if (response.ok) {
        console.log(`File uploaded successfully for resource with ID ${resourceId}`);
        // Fetch the updated resources list
        await fetchCreatedResources();
      } else {
        console.error(`Failed to upload file for resource with ID ${resourceId}`);
      }
    } catch (error) {
      console.error(error);
    }
  }

  async function handleFileUpload(event, resourceId, resourceTitle) {
    const uploadedFile = event.target.files[0];
    if (uploadedFile) {
      await uploadFile(resourceId, uploadedFile, resourceTitle);
    }
  }

</script>

<main>
  <div id="container">
    <h1>Create Resource</h1>

    <div id="navigation">
      <form on:submit="{createResource}">
        <label>
          <p>Title:</p>
          <input type="text" placeholder="Name of the Resource" bind:value="{title}" required />
        </label>
        <label>
          <p>Author:</p>
          <input type="text" placeholder="Fullname of the author" bind:value="{author}" required />
        </label>
        <label>
          <p>Year:</p>
          <input type="text" placeholder="JJJJ" bind:value="{year}" required />
        </label>
        <label>
          <p>Types:</p>
          <div class="field-with-popover">
            <input
              type="text"
              placeholder="e.g. Book, E-Book, Video,..."
              bind:value="{types}"
              required
            />
            {#if existingTypes.length > 0}
              <button
                class="question-mark"
                on:click={toggleTypeOptions}
              >
                ?
              </button>
            {/if}
          </div>
        </label>
        <label>
          <p>Code:</p>
          <input type="text" placeholder="e.g. 1234" bind:value="{code}" required />
        </label>
        <label>
          <p>Categories:</p>
          <div class="field-with-popover">
            <input
              type="text"
              placeholder="e.g. Biography"
              bind:value="{categories}"
              required
            />
            {#if existingCategories.length > 0}
              <button
                class="question-mark"
                on:click={toggleCategoryOptions}
              >
                ?
              </button>
            {/if}
          </div>
        </label>
        <label>
          <p>Link:</p>
          <input type="text" placeholder="e.g. Mediaverse.com" bind:value="{link}" required />
        </label>
        
        <label>
          <p>Description:</p>
          <textarea
            placeholder="e.g. Summary"
            bind:value="{description}"
            required
          ></textarea>
        </label>
        <div id="footer1">
          <p></p>
          <button type="submit">Create Resource</button>
        </div>
      </form>
    </div>

    <!-- Category Popover -->
    {#if showCategoryOptions && existingCategories.length > 0}
      <div class="popover">
        {#each existingCategories as category}
          <button on:click={() => { categories = `${categories}${categories ? ', ' : ''}${category.name}`; }}>
            {category.name}
          </button>
        {/each}
        <button on:click={() => { categories = `${categories}${categories ? ', ' : ''}`; toggleCategoryOptions(); }}>
          Create New Category
        </button>
      </div>
    {/if}

    <!-- Type Popover -->
    {#if showTypeOptions && existingTypes.length > 0}
      <div class="popover">
        {#each existingTypes as type}
          <button on:click={() => { types = `${types}${types ? ', ' : ''}${type.name}`; }}>
            {type.name}
          </button>
        {/each}
        <button on:click={() => { types = `${types}${types ? ', ' : ''}`; toggleTypeOptions(); }}>
          Create New Type
        </button>
      </div>
    {/if}
    

    <div id="resourcesbox">
    <!-- Display created resources -->
      {#if createdResources.length > 0}
      <h1>Created Resources</h1>
      <ul>
        {#each createdResources as resource}
          <li>
            <p>Title: {resource.title}</p>
            <p>Author: {resource.author}</p>
            <p>Year: {resource.year}</p>
            <p>Link: {resource.link}</p>
            <p>Code: {resource.code}</p>
            <p>Categories: {#each resource.categories as category}{category.name}, {/each}</p>
            <p>Types: {#each resource.types as type}{type.name}, {/each}</p>
            <p>Description: {resource.description}</p>
            <p>file: {resource.file}</p>
            <label>
              Upload a new file:
              <input type="file" accept=".pdf,.doc,.docx,.txt" on:change="{(e) => handleFileUpload(e, resource.id, resource.title)}" />
            </label>
          </li>
        {/each}
      </ul>
    {/if}
  </div>
  </div>
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
    border-radius: 15px;
    display: flex;
    align-items: center;
  }

  div {
    margin-bottom: 20px;
  }

  label {
      display: inline-grid;
      grid-template-columns: 100px 300px;
      grid-template-rows: 80px;
      vertical-align: middle;
    }

  input {
      width: 200px;
      height: 25px;
      border: 1px solid #ddd;
      background-color: #fff;
      vertical-align: bottom;
      color: #000000;
  }

  button[type="submit"] {
      cursor: pointer;
    border-radius: 2em;
    color: #fff;
    background: linear-gradient(to right, #08243c, #185792);
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
      background-color: #74e1fc;
    }

  p {
      padding-top: 0;
      line-height: 1.8;
      color: #ffffff;
      text-align: left;
      vertical-align: middle;
  }


  h1, h2 {
    font-family: "Arial", sans-serif;
    text-transform: none;
    letter-spacing: 1px;
  }

  textarea {
    background-color: white;
    font-family: "Arial", sans-serif;
    color: #000000
  }

  div#navigation {
      float: left;
      width: 1000px;
      padding-top: 2rem;
  }



  div#footer1 {
      clear: both;
      width: 100%;
      margin-bottom: 1rem;
  }

  div#container {
    padding-top: 1rem;
    text-align: center;
  }

 div.field-with-popover {
  display: grid;
  grid-template-rows: 35px 40px;
  text-align: left;
 }

div#resourcesbox {
  width: 1000px;
  text-align: center;
  margin-top: 30px;
}
</style>
