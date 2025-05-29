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

  function makeSearch() {
    window.location.assign(`/search?q=${query}`);
  }

  async function imFeelingLucky() {
    try {
      let res = await fetch(`/api/lucky`);
      if (!res.ok) {
        throw new Error(await res.text());
      }

      let url = await res.json();

      window.open(url["url"]);

    } catch (err) {
      console.error(err);
      alert("Something went wrong...");
    }
  }
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
      <button id="search-btn" disabled={query.length <= 0} on:click={makeSearch}>Search</button>
      <button id="lucky-btn" on:click={imFeelingLucky}>I'm Feeling Lucky!</button>
    </div>
  </div>
  <p id="credit">
    <small>&copy; <a href="https://hekate.neocities.org">I made this</a> in 2024</small>
  </p>
  <footer>
    <p>Bugs?  Problems?  Report them <a href="https://github.com/hekate2/archivedive/issues">here</a></p>
    <p><a href="/about">What even is this thing??</a></p>
    <p><a href="/donate">Help out w/ hosting costs</a></p>
  </footer>
</main>

<style>

  footer p {
    margin: 0;
  }

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
    max-width: 600px;
    margin: 0 auto;
    width: calc(100vw - 40px);
  }

  footer {
    position: absolute;
    bottom: 0;
    display: flex;
    font-size: small;
    margin: 10px;
  }

  footer a {
    color: lime;
  }

  @media (min-width: 576px) {
    footer > p:not(:last-of-type)::after {
      content: "|";
      margin: 0 5px;
    }
  }

  @media (max-width: 576px) {
    footer {
      flex-direction: column;
      width: calc(100vw - 20px);
      text-align: right;
      color: grey;
    }

    footer a {
      color: grey;
    }
  }
</style>