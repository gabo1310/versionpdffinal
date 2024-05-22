<!-- 
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
</style> 
 -->
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

    let useStreaming = !!localStorage.getItem('streaming');
    let pdfs: { id: string, name: string }[] = [];
    let selectedPDFs: string[] = [];
    let dropdownOpen = false;
    let showAlert = false;
    let showConfirmation = false;

    $: localStorage.setItem('streaming', useStreaming ? 'true' : '');
    $: activeConversation = $store.activeConversationId ? getActiveConversation() : null;

    async function fetchPDFIds() {
        try {
            const response = await fetch('/api/pdfs');
            pdfs = await response.json();
            // Seleccionar todos los PDFs por defecto
            selectedPDFs = pdfs.map(pdf => pdf.id);
        } catch (error) {
            console.error('Error fetching PDFs:', error);
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
            selectedPDFs = selectedPDFs.filter(id => id !== value);
        }
        console.log("Selected PDFs:", selectedPDFs);
    }

    async function handleSendSelection() {
        if (selectedPDFs.length === 0) {
            showAlert = true;
            return;
        }
        showAlert = false;
        console.log("Sending selected PDFs to backend:", selectedPDFs);
        try {
            const response = await fetch('/api/pdfs/selected-pdfs', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ pdf_ids: selectedPDFs })
            });
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            showConfirmation = true;
        } catch (error) {
            console.error('Error sending selected PDFs:', error);
        }
    }

    function toggleDropdown() {
        dropdownOpen = !dropdownOpen;
        if (dropdownOpen) {
            showAlert = false;
        }
    }

    function closeConfirmation() {
        showConfirmation = false;
    }

    onMount(() => {
        fetchConversations(documentId);
        fetchPDFIds();
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
                    {#each pdfs as pdf, index}
                        <div>
                            <input type="checkbox" id={`pdf${index + 1}`} value={pdf.id} on:change={handlePDFChange} checked={selectedPDFs.includes(pdf.id)} />
                            <label for={`pdf${index + 1}`}>{pdf.name}</label>
                        </div>
                    {/each}
                    <button class="mt-2 rounded text-sm border border-blue-500 px-2 py-0.5" on:click={handleSendSelection}>
                        Enviar Selección
                    </button>
                </div>
            {/if}
            <ConversationSelect conversations={$store.conversations} />
            <button class="rounded text-sm border border-blue-500 px-2 py-0.5" on:click={handleNewChat}>
                Nuevo chat
            </button>
        </div>
    </div>
    <div class="flex flex-col flex-1 px-3 py-2 overflow-y-scroll">
        {#if showAlert}
            <div class="alert alert-danger">
                Debes seleccionar al menos un PDF antes de enviar.
            </div>
        {/if}
        {#if showConfirmation}
            <div class="alert alert-success">
                Lista enviada. <button on:click={closeConfirmation}>OK</button>
            </div>
        {/if}
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
    .alert-success {
        color: #155724;
        background-color: #d4edda;
        border-color: #c3e6cb;
    }
</style>
