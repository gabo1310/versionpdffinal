<script lang="ts">
    export let isOpen = false;
    export let onClose = () => {};

    function closeModal() {
        onClose();
    }

    function handleKeydown(event: KeyboardEvent) {
        if (event.key === "Escape") {
            closeModal();
        }
    }
</script>

{#if isOpen}
<div class="modal-overlay" on:click={closeModal} on:keydown={handleKeydown} tabindex="-1">
    <div class="modal-content" on:click|stopPropagation>
        <slot></slot>
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

    button {
        margin-top: 1rem;
    }
</style>
