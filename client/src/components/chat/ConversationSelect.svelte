<!-- <script lang="ts">
	import type { Conversation } from '$s/chat';
	import { onMount } from 'svelte';
	import { setActiveConversationId } from '$s/chat';

	export let conversations: Conversation[] = [];
	let isOpen = false;

	async function handleClick(conversation: Conversation) {
		isOpen = false;
		setActiveConversationId(conversation.id);
	}

	function getFirstMessage(conversation: Conversation): string {
		const firstMessage = conversation.messages?.[0]?.content || '';
		return firstMessage.length > 0 ? firstMessage : ' ';
	}

	onMount(() => {
		window.addEventListener('click', (e: any) => {
			if (e.target && !e.target.closest('.relative')) {
				isOpen = false;
			}
		});
	});
</script>

<div class="relative inline-block text-left">
	<div>
		<button
			on:click={() => (isOpen = !isOpen)}
			type="button"
			class="inline-flex justify-center w-full px-4 py-2 text-sm font-medium text-white bg-blue-600 border border-transparent rounded-md hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
			id="options-menu"
			aria-haspopup="true"
			aria-expanded="true"
		>
			Historial
			<svg
				class="-mr-1 ml-2 h-5 w-5"
				xmlns="http://www.w3.org/2000/svg"
				viewBox="0 0 20 20"
				fill="currentColor"
				aria-hidden="true"
			>
				<path
					fill-rule="evenodd"
					d="M5.293 7.293a1 1 0 011.414 0L10 10.586l3.293-3.293a1 1 0 111.414 1.414l-4 4a1 1 0 01-1.414 0l-4-4a1 1 0 010-1.414z"
					clip-rule="evenodd"
				/>
			</svg>
		</button>
	</div>

	{#if isOpen}
		<div
			class="origin-top-right overflow-y-scroll absolute right-0 mt-2 w-56 rounded-md shadow-lg bg-white ring-1 ring-black ring-opacity-5"
			style="max-width: 250px; max-height: 250px;"
		>
			<div class="py-1" role="menu" aria-orientation="vertical" aria-labelledby="options-menu">
				{#each conversations as conversation (conversation.id)}
					<div
						class="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-100 hover:text-gray-900"
						on:click={() => handleClick(conversation)}
						on:keypress={() => {}}
					>
						{getFirstMessage(conversation)}
					</div>
				{/each}
			</div>
		</div>
	{/if}
</div>

 -->


 <script lang="ts">
	import type { Conversation } from '$s/chat';
	import { onMount } from 'svelte';
	import { setActiveConversationId } from '$s/chat';

	export let conversations: Conversation[] = [];
	let isOpen = false;

	async function handleClick(conversation: Conversation) {
		isOpen = false;
		setActiveConversationId(conversation.id);
	}

	function getFirstMessage(conversation: Conversation): string {
		const firstMessage = conversation.messages?.[0]?.content || '';
		return firstMessage.length > 0 ? firstMessage : ' ';
	}

	onMount(() => {
		window.addEventListener('click', (e: any) => {
			if (e.target && !e.target.closest('.relative')) {
				isOpen = false;
			}
		});
	});
</script>

<div class="relative inline-block text-left">
	<div>
		<button
			on:click={() => (isOpen = !isOpen)}
			type="button"
			class="inline-flex justify-center w-full px-4 py-2 text-sm font-medium text-white bg-blue-600 border border-transparent rounded-md hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
			id="options-menu"
			aria-haspopup="true"
			aria-expanded="true"
		>
			Historial
			<svg
				class="-mr-1 ml-2 h-5 w-5"
				xmlns="http://www.w3.org/2000/svg"
				viewBox="0 0 20 20"
				fill="currentColor"
				aria-hidden="true"
			>
				<path
					fill-rule="evenodd"
					d="M5.293 7.293a1 1 0 011.414 0L10 10.586l3.293-3.293a1 1 0 111.414 1.414l-4 4a1 1 0 01-1.414 0l-4-4a1 1 0 010-1.414z"
					clip-rule="evenodd"
				/>
			</svg>
		</button>
	</div>

	{#if isOpen}
		<div
			class="origin-top-right overflow-y-scroll absolute right-0 mt-2 w-56 rounded-md shadow-lg bg-white ring-1 ring-black ring-opacity-5"
			style="max-width: 250px; max-height: 250px;"
		>
			<div class="py-1" role="menu" aria-orientation="vertical" aria-labelledby="options-menu">
				{#each conversations as conversation (conversation.id)}
					<div
						class="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-100 hover:text-gray-900 conversation-item"
						on:click={() => handleClick(conversation)}
						on:keypress={() => {}}
					>
						{getFirstMessage(conversation)}
					</div>
				{/each}
			</div>
		</div>
	{/if}
</div>

<style>
    .dropdown-menu {
        position: absolute;
        top: 100%;
        left: 0;
        background-color: white;
        border: 1px solid #999; /* Grosor y color de la línea */
        border-radius: 4px;
        box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
        padding: 10px;
        z-index: 10;
    }
    .dropdown-menu div {
        border-top: 1px solid #999; /* Línea superior */
        border-bottom: 1px solid #999; /* Línea inferior */
        padding: 8px 0; /* Espacio entre las líneas y el contenido */
    }
    .alert {
        margin-bottom: 1rem;
        padding: 0.75rem 1.25rem;
        border: 1px solid transparent;
        border-radius: 0.25rem;
    }
    .alert-danger {
        color: #721c24;
        background-color: #f8d7da;
        border-color: #f5c6cb;
    }
    .conversation-item {
        border-top: 1px solid #999; /* Línea superior */
        border-bottom: 1px solid #999; /* Línea inferior */
        padding: 8px 0; /* Espacio entre las líneas y el contenido */
    }
</style>
