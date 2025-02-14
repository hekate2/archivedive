<script>
// @ts-nocheck

  import { onMount } from "svelte";
  import { page } from '$app/stores';
    import { pushState } from "$app/navigation";

  // Fetch query from URL params
  let q = $page.url.searchParams.get('q');
  let searchresults = [];
  let searchTime = 0;

  onMount(() => {
    search(q);
  });

  // @ts-ignore
  async function search(query) {
    try {
      if (!query || query.length === 0) {
        throw new Error("No search query provided");
      }

      // TODO: loading

      let startTime = Date.now();
      let res = await fetch(`http://127.0.0.1:5000/search?q=${query}`);

      if (!res.ok) {
        throw new Error(await res.text());
      }

      searchresults = await res.json();
      searchTime = Date.now() - startTime;

      const url = new URL(window.location.href);
      url.searchParams.set('q', query);
      pushState(url);
    } catch (err) {
      console.error(err);
    }
  }
</script>

<main>
  <div id="search-bar">
    <a href="/">
      <h1>AD</h1>
    </a>
    <input type="text" placeholder="Enter a search query" bind:value={q} />
    <button id="search-button" on:click={() => search(q)}>Search!</button>
  </div>
  {#if searchresults.length > 0}
    <p id="results-count">{searchresults.length} results found in {searchTime}ms</p>
    <ul id="results">
      {#each searchresults as result}
        <li class="result">
          <a class="site-title" href={result[1]}>{result[0]}</a>
          <a class="site-link" href={result[1]}>{result[1]}</a>
          <p>{result[2]}</p>
        </li>
      {/each}
    </ul>
  {:else}
    <p>No results found.</p>
  {/if}
</main>

<style>
  main {
    max-width: 600px;
    margin: 0 auto;
  }

  #search-bar a {
    text-decoration: none;
  }

  h1 {
    font-family: 'Fontdiner Swanky', serif;
    color: red;
    font-weight: normal;
  }

  #search-bar {
    display: flex;
    align-items: center;
  }

  #search-bar input {
    margin: 10px;
    border: 2px solid chartreuse;
    padding: 7px;
    color: white;
    font-family: 'Courier';
    background-color: transparent;
    flex-grow: 1;
    flex-shrink: 1;
    outline: none;
  }

  #search-bar h1 {
    margin-right: 10px;
  }

  #search-button {
    background-color: chartreuse;
    padding: 5px;
    color: black;
    border: 3px outset chartreuse;
    cursor: pointer;
  }

  #results-count {
    color: red;
    font-family: 'Verdana';
    font-size: 10px;
  }

  #results {
    padding: 0;
    list-style-type: none;
    font-family: 'Verdana';
  }

  #results a.site-title  {
    font-size: 15px;
    color: chartreuse;
    font-weight: bold;
  }

  #results a.site-link {
    color: cornflowerblue;
    font-size: 12px;
    margin: 5px 0;
  }

  #results p {
    font-size: 12px;
    margin: 0;
  }

  .result {
    display: flex;
    flex-direction: column;
    margin: 10px 0;
    margin-bottom: 20px;
  }
</style>