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
    import Modal from '$c/chat/Modal.svelte';
    import PromptModal from '$c/chat/PromptModal.svelte'; // Importar el nuevo componente modal

    export let onSubmit: (text: string, useStreaming: boolean) => void;
    export let documentId: number;

    let useStreaming = true; // Mantener habilitado por defecto
    localStorage.setItem('streaming', 'true'); // Asegurar que esté habilitado en el almacenamiento local
    let pdfs: { id: string, name: string }[] = [];
    let selectedPDFs: string[] = [];
    let dropdownOpen = false;
    let showAlert = false;
    let showConfirmation = false;
    let isOpen = false; // Definir la variable isOpen para el modal
    let showPromptModal = false; // Definir la variable para mostrar el modal del prompt
    let promptText = ""; // Variable para almacenar el texto del prompt

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
            isOpen = true; // Mostrar el modal

            // Cerrar el menú desplegable
            dropdownOpen = false;

            // Configurar temporizador para cerrar el modal después de 2 segundos
            setTimeout(() => {
                isOpen = false; // Cerrar el modal
            }, 2000);

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
        isOpen = false; // Cerrar el modal
    }

    function openPromptModal() {
        showPromptModal = true;
    }

    function closePromptModal() {
        showPromptModal = false;
    }

    function handleSendPrompt() {
        // Aquí puedes agregar la lógica para enviar el prompt al backend en el futuro
        console.log("Prompt text:", promptText);
        closePromptModal();
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
        <div class="flex gap-2 items-center relative">
            <button class="rounded text-sm border border-blue-500 px-2 py-0.5" on:click={openPromptModal}>
                Prompt
            </button>
            <button class="rounded text-sm border border-blue-500 px-2 py-0.5" on:click={toggleDropdown}>
                PDFs
            </button>
            {#if dropdownOpen}
                <div class="dropdown-menu">
                    {#each pdfs as pdf, index}
                        <div class="dropdown-item">
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
                New chat
            </button>
        </div>
    </div>
    <div class="flex flex-col flex-1 px-3 py-2 overflow-y-scroll">
        {#if showAlert}
            <div class="alert alert-danger">
                Debes seleccionar al menos un PDF antes de enviar.
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

<Modal {isOpen} on:close={closeConfirmation}>
    Lista enviada. OK
</Modal>

<PromptModal {showPromptModal} {promptText} on:send={handleSendPrompt} on:close={closePromptModal} />

<style>
    .dropdown-menu {
        position: absolute;
        top: 100%;
        left: 0;
        background-color: white;
        border: 2px solid #999; /* Cambia el grosor y el color de la línea */
        border-radius: 4px;
        box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
        padding: 10px;
        z-index: 10;
    }
    .dropdown-item {
        border-top: 2px solid #999; /* Línea superior */
        border-bottom: 2px solid #999; /* Línea inferior */
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
        border-top: 2px solid #999; /* Línea superior */
        border-bottom: 2px solid #999; /* Línea inferior */
        padding: 8px 0; /* Espacio entre las líneas y el contenido */
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
    import Modal from '$c/chat/Modal.svelte';
    import PromptModal from '$c/chat/promptModal.svelte'; // Importar el nuevo componente modal

    export let onSubmit: (text: string, useStreaming: boolean) => void;
    export let documentId: number;

    let useStreaming = !!localStorage.getItem('streaming');
    let pdfs: { id: string, name: string }[] = [];
    let selectedPDFs: string[] = [];
    let dropdownOpen = false;
    let showAlert = false;
    let showConfirmation = false;
    let isOpen = false; // Definir la variable isOpen para el modal
    let showPromptModal = false; // Definir la variable para mostrar el modal del prompt
    let promptText = ""; // Variable para almacenar el texto del prompt
    let useVoice = true; // Variable para el checkbox de voz

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
            isOpen = true; // Mostrar el modal

            // Cerrar el menú desplegable
            dropdownOpen = false;

            // Configurar temporizador para cerrar el modal después de 2 segundos
            setTimeout(() => {
                isOpen = false; // Cerrar el modal
            }, 2000);

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
        isOpen = false; // Cerrar el modal
    }

    function openPromptModal() {
        showPromptModal = true;
    }

    function closePromptModal() {
        showPromptModal = false;
    }

    function handleSendPrompt() {
        // Aquí puedes agregar la lógica para enviar el prompt al backend en el futuro
        console.log("Prompt text:", promptText);
        closePromptModal();
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
            <!-- Eliminado el checkbox de stream -->
        </div>
        <div class="flex gap-2 items-center relative">
            <button class="rounded text-sm border border-blue-500 px-2 py-0.5" on:click={openPromptModal}>
                Prompt
            </button>
            <button class="rounded text-sm border border-blue-500 px-2 py-0.5" on:click={toggleDropdown}>
                PDFs
            </button>
            {#if dropdownOpen}
                <div class="dropdown-menu">
                    {#each pdfs as pdf, index}
                        <div class="dropdown-item">
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
                New chat
            </button>
            <label class="inline-flex items-center ml-2">
                <input type="checkbox" checked={useVoice} on:change="{() => useVoice = !useVoice}" />
                <span class="ml-2">Voz</span>
            </label>
        </div>
    </div>
    <div class="flex flex-col flex-1 px-3 py-2 overflow-y-scroll">
        {#if showAlert}
            <div class="alert alert-danger">
                Debes seleccionar al menos un PDF antes de enviar.
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

<Modal {isOpen} on:close={closeConfirmation}>
    Lista enviada. OK
</Modal>

<PromptModal {showPromptModal} {promptText} on:send={handleSendPrompt} on:close={closePromptModal} />

<style>
    .dropdown-menu {
        position: absolute;
        top: 100%;
        left: 0;
        background-color: white;
        border: 2px solid #999; /* Cambia el grosor y el color de la línea */
        border-radius: 4px;
        box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
        padding: 10px;
        z-index: 10;
    }
    .dropdown-item {
        border-top: 2px solid #999; /* Línea superior */
        border-bottom: 2px solid #999; /* Línea inferior */
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
        border-top: 2px solid #999; /* Línea superior */
        border-bottom: 2px solid #999; /* Línea inferior */
        padding: 8px 0; /* Espacio entre las líneas y el contenido */
    }
</style>
