<script>
    // code to get the information to be shown
</script>

<div id="container">
    <div class="picture">
        <img src="./public/41AwrxBY38L.jpg" alt="photo" />
    </div>
    <div class="text">
        <div id="head">
            <h2><bold>title</bold>, author, year</h2>
        </div>
        <div id="description">
            <p>
                description of the element,description of the element,
                description of the element,description of the element,
                description of the element,description of the element,
                description of the element,description of the element,
            </p>
        </div>
        <div id="info">
            <h4>categories , type</h4>
        </div>
    </div>
</div>

<style>
    /* Styles for the container box */
    div#container {
        width: 600px;
        margin: 0 auto;
        padding: 20px;
        background-color: rgba(255, 255, 255, 0.8);
        border-radius: 10px;
        box-shadow: 0 2px 6px rgba(0, 0, 0, 0.15);
        display: flex;
    }
    .picture img {
        width: 200px;
        height: 250px;
        object-fit: cover;
        border-radius: 10px;
    }
    .text {
        margin-left: 20px;
        font-family: "Arial", sans-serif; /* Use any desired font family */
        font-size: 15px; /* Adjust the font size as per the metro sign style */
        color: #526069; /* Adjust the font color as per the metro sign style */
        text-transform: none;
        letter-spacing: 1px; /* Adjust the letter spacing as per the metro sign style */
    }
</style>
