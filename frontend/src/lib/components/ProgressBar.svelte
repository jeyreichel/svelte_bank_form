<script>
    export let step = 1
</script>
<div class="wizard-progress mb-10">
    <div class="step" class:in-progress={step<=4} class:complete={step>4}>
    </div>
    <div class="step" class:in-progress={step>4 & step<=6} class:complete={step>6}>
        <div class="bar-title">Projet</div>
        <div class="node"></div>
    </div>
    <div class="step" class:complete={step>=7}>
        <div class="bar-title">Situation</div>
        <div class="node"></div>
    </div>
    <div class="step" class:complete={step>=7}>
        <div class="bar-title">Coordonnées</div>
        <div class="node"></div>
    </div>
</div>
<style>
    .wizard-progress {
        display: table;
        width: 100%;
        table-layout: fixed;
        position: relative;
    }

    .wizard-progress .step {
        display: table-cell;
        vertical-align: top;
        overflow: visible;
        position: relative;
        font-size: 14px;
        color: #000;
        font-weight: bold;
    }

    .wizard-progress .step .bar-title {
        right: 15%;
        position: relative;

    }

    .wizard-progress .step:not(:last-child):before {
        content: "";
        display: block;
        position: absolute;
        left: 50%;
        top: 37px;
        background-color: #F5F5F6;
        height: 6px;
        width: 100%;
    }

    .wizard-progress .step .node {
        display: inline-block;
        border: 2px solid #fff;
        background-color: #fff;
        border-radius: 18px;
        height: 18px;
        width: 18px;
        position: absolute;
        top: 31px;
        left: 51%;
        margin-left: -18px;
    }

    .wizard-progress .step.complete:before {
        background-color: var(--color-theme-2);
    }

    .wizard-progress .step.complete .node {
        border-color: var(--color-theme-2);
        background-color: var(--color-theme-2);
    }

    .wizard-progress .step.complete .node:before {
        font-family: FontAwesome;
    }

    .wizard-progress .step.in-progress:before {
        background: var(--color-theme-2);
        background: -moz-linear-gradient(left, var(--color-theme-2) 0%, #fff 100%);
        background: -webkit-linear-gradient(left, var(--color-theme-2) 0%, #fff 100%);
        background: linear-gradient(to right, var(--color-theme-2) 0%, #fff 100%);
    }

    .wizard-progress .step.in-progress .node {
        border-color: var(--color-theme-2);
        background-color: var(--color-theme-2);
    }
</style>