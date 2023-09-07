<!-- App.svelte -->
<script>
  import Login from './Login.svelte';
  import Register from './Register.svelte';
  import Homepage from './Homepage.svelte';
  import Bibliothekar from './Bibliothekar.svelte';
  import Header from './user/Header.svelte';
  import QrCode from './QRCode.svelte';
  import ResourceDetails from './user/ResourceDetails.svelte';
  

  let showLogin = true;
  let showRegister = false;
  let showHomepage = false;
  let showBibliothekar = false;
  let showqr = false
  let showResourceDetails = false;

  function redirectToRegistration() {
    showHomepage = false;
    showLogin = false;
    showRegister = true;
    showBibliothekar = false;
    showqr = false;
    showResourceDetails = false;
  }

  function redirectToLogin() {
    showHomepage = false;
    showLogin = true;
    showRegister = false;
    showBibliothekar = false;
    showqr = false;
    showResourceDetails = false;
  }

  function redirectToHomepage() {
    showHomepage = true;
    showLogin = false;
    showRegister = false;
    showBibliothekar = false;
    showqr = false;
    showResourceDetails = false;
  }

  function redirectToBibliothekar() {
    showHomepage = false;
    showLogin = false;
    showRegister = false;
    showBibliothekar = true;
    showqr = false;
    showResourceDetails = false;
  }

  function redirectToQrCode() {
    showHomepage = false;
    showLogin = false;
    showRegister = false;
    showBibliothekar = false;
    showqr = true;
    showResourceDetails = false;
  }

  function viewResourceDetails() {
    showHomepage = false;
    showLogin = false;
    showRegister = false;
    showBibliothekar = false;
    showqr = false;
    showResourceDetails = true;
  }


</script>

<main>

{#if showLogin}
  <Login on:showRegister={redirectToRegistration} on:showHomepage={redirectToHomepage} />
{:else if showHomepage}
  <Homepage on:showLogin={redirectToLogin} on:showBibliothekar={redirectToBibliothekar} on:showqr={redirectToQrCode} on:showResourceDetails={viewResourceDetails}/>
{:else}
  
  {#if showBibliothekar}
    <Bibliothekar on:showLogin={redirectToLogin} on:showHomepage={redirectToHomepage} />
  {:else if showqr}
    <QrCode on:showqr={redirectToQrCode}  on:showHomepage={redirectToHomepage}/>
  {:else if showResourceDetails}
    <ResourceDetails on:showResourceDetails={viewResourceDetails} on:showHomepage={redirectToHomepage}/>
  {:else}
    <Register on:showLogin={redirectToLogin} />
  {/if}
{/if}


</main>

