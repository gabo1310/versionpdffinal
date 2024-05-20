
<!-- <script lang="ts">
    import { onMount } from 'svelte';
    import {
        store,
        resetError,
        fetchConversations,
        createConversation,
        getActiveConversation
    } from '$s/chat';
    import Alert from '$c/Alert.svelte';
    import ChatInput from '$c/chat/ChatInput.svelte';
    import ChatList from '$c/chat/ChatList.svelte';
    import ConversationSelect from '$c/chat/ConversationSelect.svelte';

    export let onSubmit: (text: string, useStreaming: boolean) => void;
    export let documentId: number;

    let useStreaming = !!localStorage.getItem('streaming');
    let pdfLabels: string[] = ["PDF 1", "PDF 2", "PDF 3"];
    let selectedPDFs: string[] = [];
    let dropdownOpen = false;

    $: localStorage.setItem('streaming', useStreaming ? 'true' : '');
    $: activeConversation = $store.activeConversationId ? getActiveConversation() : null;

    function handleSubmit(event: CustomEvent<string>) {
        if (onSubmit) {
            onSubmit(event.detail, useStreaming);
        }
    }

    function handleNewChat() {
        createConversation(documentId);
    }

    function handlePDFChange(event: Event) {
        const target = event.target as HTMLInputElement;
        const { value, checked } = target;
        if (checked) {
            selectedPDFs = [...selectedPDFs, value];
        } else {
            selectedPDFs = selectedPDFs.filter(pdf => pdf !== value);
        }
        console.log("Selected PDFs:", selectedPDFs);
    }

    function toggleDropdown() {
        dropdownOpen = !dropdownOpen;
    }

    onMount(() => {
        fetchConversations(documentId);
    });
</script>

<div
    style="height: calc(100vh - 80px);"
    class="flex flex-col h-full bg-slate-50 border rounded-xl shadow"
>
    <div class="rounded-lg border-b px-3 py-2 flex flex-row items-center justify-between">
        <div class="opacity-40">
            <input id="chat-type" type="checkbox" bind:checked={useStreaming} />
            <label for="chat-type" class="italic">Streaming</label>
        </div>
        <div class="flex gap-2 items-center relative">
            <button class="rounded text-sm border border-blue-500 px-2 py-0.5" on:click={toggleDropdown}>
                PDFs
            </button>
            {#if dropdownOpen}
                <div class="dropdown-menu">
                    {#each pdfLabels as label, index}
                        <div>
                            <input type="checkbox" id={`pdf${index + 1}`} value={label} on:change={handlePDFChange} />
                            <label for={`pdf${index + 1}`}>{label}</label>
                        </div>
                    {/each}
                </div>
            {/if}
            <ConversationSelect conversations={$store.conversations} />
            <button class="rounded text-sm border border-blue-500 px-2 py-0.5" on:click={handleNewChat}>
                Nuevo chat
            </button>
        </div>
    </div>
    <div class="flex flex-col flex-1 px-3 py-2 overflow-y-scroll">
        <ChatList messages={activeConversation?.messages || []} />
        <div class="relative">
            {#if $store.error && $store.error.length < 200}
                <div class="p-4">
                    <Alert type="error" onDismiss={resetError}>
                        {$store.error}
                    </Alert>
                </div>
            {/if}
            <ChatInput on:submit={handleSubmit} />
        </div>
    </div>
</div>

<style>
    .dropdown-menu {
        position: absolute;
        top: 100%;
        left: 0;
        background-color: white;
        border: 1px solid #ccc;
        border-radius: 4px;
        box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
        padding: 10px;
        z-index: 10;
    }
    .dropdown-menu div {
        margin-bottom: 5px;
    }
</style> -->


<script lang="ts">
    import { onMount } from 'svelte';
    import {
        store,
        resetError,
        fetchConversations,
        createConversation,
        getActiveConversation
    } from '$s/chat';
    import Alert from '$c/Alert.svelte';
    import ChatInput from '$c/chat/ChatInput.svelte';
    import ChatList from '$c/chat/ChatList.svelte';
    import ConversationSelect from '$c/chat/ConversationSelect.svelte';

    export let onSubmit: (text: string, useStreaming: boolean) => void;
    export let documentId: number;
    export let userId: number; // Añadido para identificar al usuario

    let useStreaming = !!localStorage.getItem('streaming');
    let pdfLabels: string[] = [];
    let selectedPDFs: string[] = [];
    let dropdownOpen = false;

    $: localStorage.setItem('streaming', useStreaming ? 'true' : '');
    $: activeConversation = $store.activeConversationId ? getActiveConversation() : null;

    async function fetchPDFNames() {
        try {
            const response = await fetch(`/api/user/${userId}/pdfs`);
            const data = await response.json();
            pdfLabels = data.pdfs;
        } catch (error) {
            console.error("Error fetching PDF names:", error);
        }
    }

    function handleSubmit(event: CustomEvent<string>) {
        if (onSubmit) {
            onSubmit(event.detail, useStreaming);
        }
    }

    function handleNewChat() {
        createConversation(documentId);
    }

    function handlePDFChange(event: Event) {
        const target = event.target as HTMLInputElement;
        const { value, checked } = target;
        if (checked) {
            selectedPDFs = [...selectedPDFs, value];
        } else {
            selectedPDFs = selectedPDFs.filter(pdf => pdf !== value);
        }
        console.log("Selected PDFs:", selectedPDFs);
    }

    function toggleDropdown() {
        dropdownOpen = !dropdownOpen;
    }

    onMount(() => {
        fetchConversations(documentId);
        fetchPDFNames(); // Llamada para obtener los nombres de los PDFs
    });
</script>

<div
    style="height: calc(100vh - 80px);"
    class="flex flex-col h-full bg-slate-50 border rounded-xl shadow"
>
    <div class="rounded-lg border-b px-3 py-2 flex flex-row items-center justify-between">
        <div class="opacity-40">
            <input id="chat-type" type="checkbox" bind:checked={useStreaming} />
            <label for="chat-type" class="italic">Streaming</label>
        </div>
        <div class="flex gap-2 items-center relative">
            <button class="rounded text-sm border border-blue-500 px-2 py-0.5" on:click={toggleDropdown}>
                PDFs
            </button>
            {#if dropdownOpen}
                <div class="dropdown-menu">
                    {#each pdfLabels as label, index}
                        <div>
                            <input type="checkbox" id={`pdf${index + 1}`} value={label} on:change={handlePDFChange} />
                            <label for={`pdf${index + 1}`}>{label}</label>
                        </div>
                    {/each}
                </div>
            {/if}
            <ConversationSelect conversations={$store.conversations} />
            <button class="rounded text-sm border border-blue-500 px-2 py-0.5" on:click={handleNewChat}>
                Nuevo chat
            </button>
        </div>
    </div>
    <div class="flex flex-col flex-1 px-3 py-2 overflow-y-scroll">
        <ChatList messages={activeConversation?.messages || []} />
        <div class="relative">
            {#if $store.error && $store.error.length < 200}
                <div class="p-4">
                    <Alert type="error" onDismiss={resetError}>
                        {$store.error}
                    </Alert>
                </div>
            {/if}
            <ChatInput on:submit={handleSubmit} />
        </div>
    </div>
</div>

<style>
    .dropdown-menu {
        position: absolute;
        top: 100%;
        left: 0;
        background-color: white;
        border: 1px solid #ccc;
        border-radius: 4px;
        box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
        padding: 10px;
        z-index: 10;
    }
    .dropdown-menu div {
        margin-bottom: 5px;
    }
</style>


