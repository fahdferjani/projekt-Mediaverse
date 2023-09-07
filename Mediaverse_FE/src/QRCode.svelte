<script>
    import { Html5Qrcode } from 'html5-qrcode';
    import { onMount } from 'svelte';
    import { Link } from 'svelte-navigator';
    



    let scanning = false
    let html5Qrcode

    onMount(init)

    function init() {
        html5Qrcode = new Html5Qrcode('reader')
    }

    function start() {
        html5Qrcode.start(
            { facingMode: 'environment' },
            {
                fps: 10,
                qrbox: { width: 200, height: 200 },
            },
            onScanSuccess,
            onScanFailure
        )
        scanning = true
    }

    async function stop() {
        await html5Qrcode.stop()
        scanning = false
    }

    /**
     * @param {any} decodedText
     * @param {any} decodedResult
     */
    function onScanSuccess(decodedText, decodedResult) {
        alert(`Code matched = ${decodedText}`)
        console.log(decodedResult)
    }

    /**
     * @param {any} error
     */
    function onScanFailure(error) {
        console.warn(`Code scan error = ${error}`)
    }



</script>

<main>

    <reader id="reader"/> 
    <div id="box">
        {#if scanning}
            <button on:click={stop}>stop</button>
        {:else}
            <button on:click={start}>start</button>
        {/if}
        
            <Link to="/ResourceDetails"><button>View Resource</button></Link>
    </div>

   
</main>

<style>
    main {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        gap: 20px;
        margin: 0;
        padding: 0;
        padding-bottom: 1rem;
        height: cover;
        width: cover;
        font-family: "Helvetica", sans-serif;
        line-height: 1.2em;
        background: radial-gradient(circle, #b6c4d2 10%, #355779 100%);
        justify-content: center;
        color: #dce4ec;
        line-height: 1.5;
        border-radius: 15px; /* Adjust the border radius to create a curved style */
        align-items: center;
    }

    #reader {
        width: 400px;
        height: 300px;
        padding-top: 1rem;
        background-color: #08243c;
    }
 

  #box {
    height: 200px;
    width: cover;
    padding-top: 1rem;
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