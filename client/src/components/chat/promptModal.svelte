<script lang="ts">
    export let showPromptModal: boolean;
    export let promptText: string;

    function closePromptModal() {
        showPromptModal = false;
        dispatch("close");
    }

    function handleSendPrompt() {
        dispatch("send");
    }

    import { createEventDispatcher } from "svelte";
    const dispatch = createEventDispatcher();
</script>

{#if showPromptModal}
<div class="modal-overlay" on:click={closePromptModal}>
    <div class="modal-content" on:click|stopPropagation>
        <textarea bind:value={promptText} rows="4" cols="50" placeholder="Escribe tu prompt aquí..."></textarea>
        <div class="flex justify-end mt-2">
            <button class="mr-2 rounded text-sm border border-blue-500 px-2 py-0.5" on:click={handleSendPrompt}>Enviar</button>
            <button class="rounded text-sm border border-blue-500 px-2 py-0.5" on:click={closePromptModal}>Cancelar</button>
        </div>
    </div>
</div>
{/if}

<style>
    .modal-overlay {
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: rgba(0, 0, 0, 0.5);
        display: flex;
        align-items: center;
        justify-content: center;
        z-index: 1000;
    }

    .modal-content {
        background: white;
        padding: 1rem;
        border-radius: 0.5rem;
        box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
    }

    textarea {
        width: 100%;
        border: 1px solid #ccc;
        border-radius: 0.25rem;
        padding: 0.5rem;
        font-size: 1rem;
    }

    button {
        margin-top: 1rem;
    }
</style>
