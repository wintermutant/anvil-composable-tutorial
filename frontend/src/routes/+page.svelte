<script>
	let name = $state('');
	let names = $state([]);
	let loading = $state(true);
	let error = $state('');

	const API_URL = import.meta.env.VITE_API_URL || '';

	async function fetchNames() {
		try {
			const res = await fetch(`${API_URL}/api/names`);
			const data = await res.json();
			names = data.names || [];
		} catch (e) {
			error = 'Failed to load names';
		} finally {
			loading = false;
		}
	}

	async function addName() {
		if (!name.trim()) return;
		error = '';
		try {
			const res = await fetch(`${API_URL}/api/names`, {
				method: 'POST',
				headers: { 'Content-Type': 'application/json' },
				body: JSON.stringify({ name: name.trim() })
			});
			if (res.ok) {
				name = '';
				await fetchNames();
			} else {
				error = 'Failed to add name';
			}
		} catch (e) {
			error = 'Failed to add name';
		}
	}

	fetchNames();
</script>

<main>
	<h1>Welcome to Anvil Composable</h1>

	<section>
		<h2>Guest Book</h2>
		<form onsubmit={(e) => { e.preventDefault(); addName(); }}>
			<input type="text" bind:value={name} placeholder="Enter your name" />
			<button type="submit">Sign</button>
		</form>
		{#if error}
			<p class="error">{error}</p>
		{/if}
	</section>

	<section>
		<h3>Signatures</h3>
		{#if loading}
			<p>Loading...</p>
		{:else if names.length === 0}
			<p>No signatures yet. Be the first!</p>
		{:else}
			<ul>
				{#each names as n}
					<li>{n}</li>
				{/each}
			</ul>
		{/if}
	</section>
</main>

<style>
	main {
		max-width: 600px;
		margin: 0 auto;
		padding: 2rem;
		font-family: system-ui, sans-serif;
	}

	h1 {
		color: #333;
		text-align: center;
	}

	form {
		display: flex;
		gap: 0.5rem;
		margin-bottom: 1rem;
	}

	input {
		flex: 1;
		padding: 0.5rem;
		font-size: 1rem;
		border: 1px solid #ccc;
		border-radius: 4px;
	}

	button {
		padding: 0.5rem 1rem;
		font-size: 1rem;
		background: #4a90a4;
		color: white;
		border: none;
		border-radius: 4px;
		cursor: pointer;
	}

	button:hover {
		background: #3a7a94;
	}

	ul {
		list-style: none;
		padding: 0;
	}

	li {
		padding: 0.5rem;
		border-bottom: 1px solid #eee;
	}

	.error {
		color: red;
	}
</style>
