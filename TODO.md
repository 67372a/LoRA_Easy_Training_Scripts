# ToDo list for UI changes

## General

### User Experience

- [ ] Find out how to reduce the margin of the big expander elements

- [ ] ~~Add vertical separator (Line) to visually separate Layouts better~~ | BaseUI
  - is currently removed because idk yet how to make the QGroupBoxes "take it as middle", also the line seems off in qt-material themes

- [x] Use QGridLayout instead of 3 QHBoxLayouts for model checkboxes, makes them look more orderly

### Dev

- [ ] Fix .ui Pyside6/Qt Designer files being out of sync with generated .py files
  - [x] Fix BaseUI.ui
  - [x] Fix MainUI.ui
  - [ ] ... check other files ...

- [ ] Find out how to make designer not save file with *_ui.py suffix and instead reuse .ui file's file name

### Think about/needs testing/confirmation

- [ ] Max Token Length: Allow any number or multiple of 75, apparently code has no limit for it but UI and CLI arg do, higher might work, at users discretion | BaseUI
- [ ] VAE Reflection checkbox would reduce minimum width for the UI which could lead to better experience since it allows smaller window, especially without compact mode using material theme, see FM/RF in new implementations | BaseUI
- [ ] Compact Mode (Material): Make it default?

## Change name to more correct and/or commonly used alternatives

- [ ] Keep Tokens -> Keep Tags
  - [x] Keep Tokens Separator -> Keep Tags Separator | BaseUI
    - [x] Update tooltip to note the change
  - [ ] Keep Tokens -> Keep Tags | SubsetUI
    - [ ] Update tooltip

- [ ] V Param to V Pred | BaseUI
  - [x] Update tooltip
- [ ] rate via epoch to (?) | Saving Args?

## Tooltips

- [ ] Add if a setting is suggested/recommended to tooltips, eg latent caching and sdpa is likely suggested, or protected tags over keep tokens/tags

- [ ] Think about adding the CLI arg each option uses to tooltip
  - [ ] Yes
  - [ ] No

- [ ] Check on following Tooltips
  - [ ] Scale V pred loss | BaseUI
  - [ ] ... find more ...

- [ ] Fill out empty/almost empty tooltips
  - [ ] High VRAM | BaseUI
  - [ ] Debiased Estimation Loss | BaseUI
  - [ ] ... find more ...

- [ ] Add and rework tooltips whereever it'll help ()

## Set new default values to accomodate newer, more commonly used standards

- [x] Width/Height default to 1024 from 512 | BaseUI
  - [ ] Contemplate: Since this was made for sd1.5 in mind, setting SDXL to default true probably bad but unlikely people will train sub 1mp model
- [ ] Cache Latents default true? | BaseUI
- [ ] SDPA default true? | BaseUI

## Implement new elements

- [ ] Global Protected Tags file | BaseUI
  - [x] Hook up global protected tags file to logic
    - [x] Make textbox disabled when checkbox is unchecked
  - [x] give selector button same 3 dot icon as base model/external vae ones
  - [ ] Add tooltip

- [ ] FlowMatch/Rectified Flow settings
  - [ ] Find out where to put it
  - Likely in BaseUI, in Model QGroupBox, as expandable element, move VAE Reflection and Debiased EL in too?

## Requires backend change (probably)

- [ ] Option to ignore or delete/overwrite existing cached latents

## Other

check generalui.py for code-set ui defaults/fallbacks

### Fixes

- [x] Keep Tokens/Tags Separator now correctly won't pass on it's value, if populated, downstream/when saving toml
- [ ] Infer values from UI instead of hardcoded dict to use UI defaults correctly
  - [x] General Args/GeneralUI
  - [ ] ... find it in the other files ...
