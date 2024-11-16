<script>
  import { onMount } from 'svelte';
  import { SearchBar } from "$lib";
  import { bounceDat } from "$lib";

  let query = "";

  /**
     * @type {HTMLParagraphElement}
     */
  let tagLine;

  onMount(() => {
		bounceDat(tagLine);
	});
</script>

<main>
  <div id="logotype">
    <h1>ArchiveDive</h1>
    <p class="wiggle" bind:this={tagLine}>
      <span></span>
      Search like it's 1999
    </p>
  </div>
  <div id="search">
    <SearchBar bind:query />
    <div id="search-btns">
      <button id="search-btn">Search</button>
      <button id="lucky-btn">I'm feeling lucky!</button>
    </div>
  </div>
  <p id="credit">
    <small>&copy; <a href="https://github.com/hekate2">I made this</a> in 2024</small>
  </p>
</main>

<style>
  #logotype {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    margin: 20px;
    user-select: none;
  }

  h1 {
    font-family: "Fontdiner Swanky", serif;
    color: crimson;
    font-weight: normal;
    font-size: 45px;
  }

  #credit a {
    color: lime;
  }

  #logotype h1,
  #logotype p {
    margin: 0;
  }

  #search-btns {
    padding: 20px;
    display: flex;
    justify-content: center;
  }

  #search-btn {
    margin-right: 5px;
    padding: 5px 10px;
    background-color: lime;
    border: 2px outset lime;
  }

  #search-btn:active {
    opacity: 0.9;
    border: 2px inset lime;
    filter: brightness(1);
  }

  #lucky-btn {
    border: 2px solid lime;
    background: transparent;
    color: lime;
  }

  #lucky-btn:active {
    color: black;
    background-color: lime;
  }

  #search-btn, #lucky-btn {
    cursor: pointer;
  }

  main {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    min-height: 100vh;
  }
</style>