<script></script>

<help>
  <div class="wrapper">
    <h1 style="margin-bottom:20%">Q&A</h1>
    <p style="margin-bottom:5%; font-size: 120%;color: black;">
      How can we help you?
    </p>

    <div class="wrap-1">
      <input type="radio" id="tab-1" name="tabs" />
      <label for="tab-1"
        ><div>What is Mediaverse?</div>
        <div class="cross" /></label
      >
      <div class="content">
        The variety of media is increasing in today's society, in the past
        mostly books were borrowed, but nowadays digital media of all kinds and
        whole hardware components are added.To keep track of the present
        information overload, our hybrid media library 'Mediaverse' can offer
        you support. In our web-based software, you can store and manage a wide
        variety of media without losing the overview or having to search for
        something for a long time. The website is accessible from any place with
        an internet connection and therefore digital media like texts and
        digitized books can be downloaded at any time. 'Mediaverse' offers the
        possibility to create a place that enables knowledge, exchange and
        collaboration in an efficient way.
      </div>
    </div>

    <div class="wrap-2">
      <input type="radio" id="tab-2" name="tabs" />
      <label for="tab-2"
        ><div>I cannot find the ressource I am searching for.</div>
        <div class="cross" /></label
      >
      <div class="content">
        Have you tried checking different types of categories and types or
        entering other information about the resource? On Mediaverse you can
        search for the items you want by simply inserting any information that
        references them, such as the year of publication or the author. Make
        sure to try the different versions if you have trouble finding a
        resource.
      </div>
    </div>

    <div class="wrap-3">
      <input type="radio" id="tab-3" name="tabs" />
      <label for="tab-3"
        ><div>I have problems managing my account.</div>
        <div class="cross" /></label
      >
      <div class="content">
        If you want to change information about your account, such as your
        associated email address or password, you can make the necessary changes
        on the account page.
      </div>
    </div>

    <div class="wrap-4">
      <input type="radio" id="tab-4" name="tabs" />
      <label for="tab-4"
        ><div>I need help using my favourites list.</div>
        <div class="cross" /></label
      >
      <div class="content">
        If you want to add a new item to your personal favorites list, search
        for it in the search engine and click the star icon to add it to your
        list! On the other hand, if you want to delete items from your list, you
        can do so by clicking the trash can icon in your list.
      </div>
    </div>

    <div class="wrap-5">
      <input type="radio" id="tab-5" name="tabs" />
      <label for="tab-5"
        ><div>I would like to make suggestions.</div>
        <div class="cross" /></label
      >
      <div class="content">
        Mediaverse has been designed to be highly responsive to changes and new
        enhancements. For any kind of suggestion you have for us, make sure to
        contact us through our email address team@irp-mediaverse.com.
      </div>
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
</help>

<style>
  
  help {
    margin: 0;
    padding: 0;
    min-height: 700px;
    width: cover;
    font-family: "Helvetica", sans-serif;
    line-height: 1.2em;
    background: radial-gradient(circle, #b6c4d2 10%, #355779 100%);
    justify-content: center;
    color: #dce4ec;
    line-height: 1.5;
    border-radius: 15px; /* Adjust the border radius to create a curved style */
    display: flex;
    flex-direction: column;
    align-items: center;
  }

  * {
    padding: 0;
    margin: 0;
    box-sizing: border-box;
    color: #3e474f;
  }

  .wrapper {

    max-width: 600px;
    width: 100%;
    margin: 10vh auto;
  }

  h1 {
    font-size: 2em;
    margin-bottom: 20px;
    text-align: center;
    color: #dce4ec;
  }

  h5 {
    color: #dce4ec;
  }

  input {
    display: none;
  }

  label {
    display: flex;
    min-width: 100%;
    height: 50px;
    cursor: pointer;
    border: 3px solid #3e474f;
    user-select: none;
    background: rgb(62, 71, 79,0.2);
  }
  

  label div:first-child {
    min-width: 100%;
    line-height: 45px;
    margin-left: 10px;
    font-size: 1.2em;
    color: rgb(220, 228, 236);
  }

  .cross {
    margin-right: 15px;
    margin-top: 3px;
  }

  .cross:before,
  .cross:after {
    content: "";
    border-top: 2px solid #3e474f;
    width: 15px;
    display: block;
    margin-top: 18px;
    transition: 0.3s;
  }

  .cross:after {
    transform: rotate(90deg);
    margin-top: -2px;
  }

  .content {
    box-sizing: border-box;
    font-size: 1em;
    margin: 10px 10px;
    max-height: 0;
    overflow: hidden;
    transition: max-height, 0.5s;
    background: radial-gradient(circle, #d2deeb 40%, #b5c3d2 70%);
    text-align: left;
  }

  input:checked ~ .content {
    max-height: 400px;
    transition: max-height, 1s;
  }

  input:checked ~ label .cross:before {
    transform: rotate(180deg);
  }

  input:checked ~ label .cross:after {
    transform: rotate(0deg);
  }
</style>
