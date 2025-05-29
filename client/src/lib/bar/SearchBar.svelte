<script lang="ts">
  // props
  export let query = '';
  let sugg:string[] = [];

  // suggests queries
  function completeSuggestions() {
    if (query) {
      sugg = [`${query} angelfire`, `What is ${query}`, `${query} geocities`, `Websites about ${query} geocities`];
    }
  }

  // Reactively call the suggestions function whenever `query` changes
  $: query, completeSuggestions();
</script>

<input
  id="search-bar"
  placeholder="Enter your query..."
  autocomplete="off"
  bind:value={query}
>
{#if query.length > 0}
  <ul id="search-sugg-box">
    {#each sugg as suggestion}
      <li class="suggestion" on:click={() => window.location.assign(`/search?q=${suggestion}`)}>
        {suggestion.split(query)[0]}
        <strong>{query}</strong>
        {suggestion.split(query)[1]}
      </li>
    {/each}
  </ul>
{/if}

<style>
  #search-bar {
    min-width: 300px;
    max-width: 500px;
    width: 50vw;
    padding: 10px;
    background-color: black;
    border: 2px solid limegreen;
    color: white;
    font-family: monospace;
    outline: none;
  }

  #search-sugg-box {
    list-style-type: none;
    margin: 10px 0;
    border: 2px solid;
    padding: 0;
    font-family: Verdana, Geneva, Tahoma, sans-serif;
    font-size: 10pt;
  }

  .suggestion {
    padding: 5px 10px;
    cursor: pointer;
  }

  .suggestion:hover {
    background-color: #ff000045;
  }

  #search-sugg-box .suggestion:last-of-type {
    padding-bottom: 10px;
  }
</style>