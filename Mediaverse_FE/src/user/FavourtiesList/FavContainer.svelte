<script>
import DisplayObject from "./DisplayObject.svelte";
</script>

<div id="example3" class="container off-bottom">
    <div class="scrollbox">
      <ul class="list">
        <li class="item"> <DisplayObject/> </li>
        <li class="item"><DisplayObject/></li>
        <li class="item"><DisplayObject/></li>
        <li class="item"><DisplayObject/></li>
        <li class="item"><DisplayObject/></li>
        <li class="item"><DisplayObject/></li>
        <li class="item"><DisplayObject/></li>
        <li class="item"><DisplayObject/></li>
        <li class="item"><DisplayObject/></li>
        <li class="item"><DisplayObject/></li>
      </ul>
    </div>
    <div class="shadow shadow-top" aria-hidden="true"></div>
    <div class="shadow shadow-bottom" aria-hidden="true"></div>
  </div>

<style lang=scss>

  #example3 {
  overflow:hidden;
  position:relative;

  .scrollbox {
    height:100%;
    overflow:auto;
  }
  .shadow {
    bottom:0;      
    left:0;
    pointer-events:none;
    position:absolute;
    right:0;
    top:0;
    transition:all .2s ease-out;
  }
  .shadow off-top {
    .shadow-top {
      box-shadow:0 1em 1em -1em black inset;
    }
  }
  .shadow off-bottom {    
    .shadow-bottom {
      box-shadow:0 -1em 1em -1em black inset;
    }
  }
}

.container {
  background-color:white;
  border:solid .5em black;
  border-radius:.5em;
  box-sizing:border-box;
  flex:0 0 30%;
  height:500px;
  margin:.5em;
  overflow:auto;
}

.list {
  list-style:none;
  margin:0;
  padding:0;
  height:100%;
}

.item {
  background-color:lightgray;
  margin-top:2%;
  padding:0.3%;
  height:auto;
}

@keyframes flash {
  0%, 100% {
    opacity:1;
  }
  50% {
    opacity:.2;
  }
}
</style>