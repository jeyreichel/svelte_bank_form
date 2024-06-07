<script lang="ts">
  export let id,
    valid,
    only_month = false;

  export let date: Date | String;

  let isFocused = false,
    not_valid = false,
    showDateErrors = false,
    showDayErrors = false,
    showMonthErrors = false,
    showBirthErrors = false,
    inputDate: Date;

  const currentDate = new Date();
  const currentMonth = new Date(date).getMonth();
  const currentDay = new Date(date).getDate();
  let day = date !== undefined ? String(currentDay) : only_month ? "01" : "",
    month =
      date !== undefined
        ? currentMonth >= 10
          ? String(currentMonth)
          : "0" + currentMonth
        : "",
    year = date !== undefined ? String(new Date(date).getFullYear()) : "",
    day_input: HTMLInputElement,
    month_input: HTMLInputElement,
    year_input: HTMLInputElement;

  $: {
    if (year && month && (day || only_month)) {
      inputDate = new Date(Number(year), Number(month), Number(day));
      not_valid =
        day !== "" &&
        month !== "" &&
        month.length == 2 &&
        year !== "" &&
        year.length == 4 &&
        valid !== "" &&
        inputDate > currentDate &&
        !isFocused;
      showDateErrors = inputDate > currentDate;

      if (!not_valid) date = new Date(Number(year), Number(month), Number(day));
    }
  }

  $: {
    if (only_month == false) {
      inputDate = new Date(Number(year), Number(month), Number(day));
      showBirthErrors =
        18 >= currentDate.getFullYear() - inputDate.getFullYear() &&
        currentDate.getFullYear() - inputDate.getFullYear() < 70;
    }
  }

  function changeFocus(day, month) {
    if (day.length === 2 && !only_month) {
      month_input.focus();
    }
    if (month.length === 2) {
      year_input.focus();
    }
  }

  const onFocus = () => {
    isFocused = true;
  };

  const onBlur = () => {
    isFocused = false;
  };

  const handleDayInput = (event) => {
    const inputDay = event.target.value;
    if (+inputDay >= 1 && +inputDay <= 31) {
      if (+inputDay < 10 && +inputDay > 3) {
        day = "0" + inputDay;
      } else {
        day = inputDay;
      }
    } else if (+inputDay === 0) {
      day = "";
    } else {
      showDayErrors = true;
    } // Allow only numeric values and limit to 2 characters
    event.target.value = day;
  };

  const handleMonthInput = (event) => {
    const inputMonth = event.target.value;
    if (+inputMonth >= 1 && +inputMonth <= 12) {
      if (+inputMonth < 10 && +inputMonth > 1) {
        month = "0" + inputMonth;
      } else {
        month = inputMonth;
      }
    } else if (+inputMonth === 0) {
      month = "";
    } else {
      showMonthErrors = true;
    } // Allow only numeric values and limit to 2 characters
    event.target.value = month;
  };

  const onClick = (day, month, year) => {
    if (day.length < 2 && month.length === 0 && !only_month) {
      day_input.focus();
    } else if (day.length === 2 && month.length < 2) {
      month_input.focus();
    } else if (month.length === 2 && year.length === 0) {
      year_input.focus();
    }
  };

  function onKeyUpAndDown(e) {
    if (e.key === "Backspace") {
      if (day.length === 2 && month.length === 2 && year.length === 0) {
        month_input.focus();
      } else if (day.length === 2 && month.length === 0 && !only_month) {
        day_input.focus();
      }
    } else {
      changeFocus(day, month);
    }
  }

  const handleKeyDown = (event) => {
    // Allow only number keys (0-9) and certain control keys (e.g., backspace, delete, arrow keys)
    const keyCode = event.keyCode || event.which;
    const allowedKeys = [8, 9, 37, 39, 46]; // Add more keycodes as needed
    if ((keyCode < 48 || keyCode > 57) && !allowedKeys.includes(keyCode)) {
      event.preventDefault();
    }
  };
</script>

<div {...$$props}>
  <label
    for={id}
    class="absolute md:text-xl text-gray-500 duration-300
                               transform -translate-y-6 translate-x-4 scale-75 origin-[0] peer-focus:left-0"
    class:isLabelValid={not_valid === false &&
      day !== "" &&
      month !== "" &&
      year !== "" &&
      showBirthErrors === false}
    class:text-red-600={showBirthErrors || showDateErrors || not_valid === true}
    class:font-medium={day !== ""}
  >
    <slot></slot>
  </label>
  <div
    {id}
    class="field-date border border-gray-300"
    on:focus={onFocus}
    on:keydown={onKeyUpAndDown}
    on:keyup={onKeyUpAndDown}
    on:blur={onBlur}
    on:click={() => onClick(day, month, year)}
    class:isValid={not_valid === false &&
      day !== "" &&
      month !== "" &&
      year !== "" &&
      showBirthErrors === false}
    class:border-red-600={showBirthErrors &&
      showDateErrors &&
      not_valid === true}
  >
    {#if !only_month}
      <input
        name="{id}_DD"
        type="text"
        placeholder="JJ"
        maxlength="2"
        tabindex="0"
        on:input={handleDayInput}
        class="field-date-input md:text-xl text-gray-500"
        bind:value={day}
        bind:this={day_input}
        on:keydown={handleKeyDown}
      />
      <span>/</span>
    {/if}
    <input
      name="{id}_MM"
      type="text"
      placeholder="MM"
      maxlength="2"
      tabindex="0"
      on:input={handleMonthInput}
      class="field-date-input md:text-xl text-gray-500"
      bind:value={month}
      bind:this={month_input}
      on:keydown={handleKeyDown}
    />
    <span>/</span>
    <input
      name="{id}_YYYY"
      type="text"
      placeholder="AAAA"
      maxlength="4"
      tabindex="0"
      class="field-date-input md:text-xl text-gray-500"
      bind:value={year}
      bind:this={year_input}
      on:keydown={handleKeyDown}
    />
  </div>

  <!-- {#if not_valid}
    <span class:text-red-600={true} class:col-span-12={true}>
      {valid["message"]}
    </span>
  {/if} -->

  {#if showDateErrors}
    <span class:text-red-600={true} class:col-span-12={true}>
      Date de première mensualité est postérieure à la date actuelle.
    </span>
  {/if}
  {#if showMonthErrors && showDayErrors}
    <span class:text-red-600={true} class:col-span-12={true}>
      Veuillez saisir correctement le format de date.
    </span>
  {/if}
  {#if showBirthErrors}
    <span class:text-red-600={true} class:col-span-12={true}>
      Le titulaire du contrat doit avoir plus de 18 ans
    </span>
  {/if}
</div>

<style>
  .field-date {
    display: flex;
    flex-wrap: wrap;
    align-items: center;
    background-color: #fff;
    border-radius: var(--border-radius);
    height: 60px;
    box-shadow: 0 4px 8px rgba(172, 186, 200, 0.1);
  }

  .field-date .field-date-input {
    flex: 1;
    border: none;
    min-width: 0;
    text-align: center;
    outline: 0;
    background-color: transparent;
  }

  input:focus {
    --tw-ring-color: none;
  }

  .isLabelValid {
    color: green;
  }

  .isValid {
    border: 1px solid green;
  }
</style>
