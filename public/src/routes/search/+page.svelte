<script>
  // @ts-nocheck
  import { onMount } from "svelte";
  import { page } from '$app/stores';
  import { pushState } from "$app/navigation";

  let q = $page.url.searchParams.get('q') || '';
  let p = 0;
  let searchresults = [];
  let searchTime = 0;
  let totalResults = 0;

  const cache = new Map(); // key: `${query}_${page}`, value: { data, time, total }

  onMount(() => {
    if (q) search(q, p);
  });

  async function search(query, pg = 0) {
    try {
      if (!query || query.length === 0) {
        throw new Error("No search query provided");
      }

      const cacheKey = `${query}_${pg}`;
      if (cache.has(cacheKey)) {
        const cached = cache.get(cacheKey);
        searchresults = cached.data;
        searchTime = cached.time;
        totalResults = cached.total;
        p = pg;
        return;
      }

      const startTime = Date.now();
      const res = await fetch(`http://localhost:5000/search?q=${encodeURIComponent(query)}&p=${pg}`);
      if (!res.ok) {
        throw new Error(await res.text());
      }

      const json = await res.json();
      const elapsedTime = Date.now() - startTime;

      searchresults = json.results;
      totalResults = json.num_results;
      searchTime = elapsedTime;
      p = pg;

      cache.set(cacheKey, {
        data: json.results,
        time: elapsedTime,
        total: json.num_results
      });

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
    <input
      type="text"
      placeholder="Enter a search query"
      bind:value={q}
      on:keydown={(e) => e.key === 'Enter' && search(q, 0)}
    />
    <button id="search-button" on:click={() => search(q)}>Search!</button>
  </div>
  {#if searchresults.length > 0}
    <p id="results-count">{totalResults} results found in {searchTime}ms</p>
    <ul id="results">
      {#each searchresults as result}
        <li class="result">
          <a class="site-title" href={result[1]}>{result[0]}</a>
          <a class="site-link" href={result[1]}>{result[1]}</a>
          <p>{result[2]}</p>
        </li>
      {/each}
    </ul>
    <button on:click={() => search(q, p - 1)} disabled={p <= 0}>Previous Page</button>
    <button on:click={() => search(q, p + 1)}>Next Page</button>
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