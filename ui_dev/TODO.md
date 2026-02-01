# ToDo list for UI changes

## General

### Dev

- [ ] Fix .ui Pyside6/Qt Designer files being out of sync with generated .py files
  - [x] BaseUI.ui
  - [x] MainUI.ui
  - [x] sub_dataset_input.ui
  - [x] sub_dataset_extra_input.ui
  - [ ] ... check other files ...

### Think about/needs testing/confirmation

- [ ] Max Token Length: Allow any number or multiple of 75, apparently code has no limit for it but UI and CLI arg do, higher might work, at users discretion | BaseUI
- [ ] Compact Mode (Material): Make it default?
- [ ] Disable Flip Augmentation when Cache Latents is checked
  - sd scripts readme says flip aug is not available when cache latents is true but the UI only disables color aug and random crop

## Tooltips

- [ ] Add if a setting is suggested/recommended to tooltips, eg latent caching and sdpa is likely suggested, or protected tags over keep tokens/tags

- [ ] Check on following Tooltips
  - [ ] Scale V pred loss | BaseUI
  - [ ] ... find more ...

- [ ] Fill out empty/almost empty tooltips
  - [ ] High VRAM | BaseUI
  - [ ] Debiased Estimation Loss | BaseUI
  - [ ] ... find more ...

- [ ] Add and rework tooltips whereever it'll help

## Set new default values to accomodate newer, more commonly used standards

- [ ] Cache Latents default true? | BaseUI
- [ ] SDPA default true? | BaseUI

## Implement new elements

- [x] Global Protected Tags file | BaseUI
  - [x] Hook up global protected tags file to logic
    - [x] Make textbox disabled when checkbox is unchecked
  - [x] give selector button same 3 dot icon as base model/external vae ones
  - [x] Tooltip

- [x] FlowMatch/Rectified Flow/Adv. VAE/Misc settings
  - [x] Find out where to put it
  - ~~Likely in BaseUI, in Model QGroupBox, as expandable element, move VAE Reflection and Debiased EL in too?~~
    - Done, ExperimentalArgsUI
  - [x] Flow Model settings: Logit Mean/std, optimal transport, shift, ts dist
  - [x] VAE: batch size, reflection, scale, shift
  - [x] Misc: Zero Cond Dropout, CFM, CFM Lambda, Debiased Estimation Loss
  - [x] Tooltips

## Requires backend change

- [ ] Option to ignore or delete/overwrite existing cached latents

## Other

### Fixes

There may be lingering issues with the stuff below because i cant make sense out of the ui logic code, usually when checked -> saved -> unchecked -> saved - issue appears, lingering args

- [ ] UI Elements passing on values to training/save toml even when unchecked, if value inputs are populated
  - [x] Flow Model GroupBox
  - [x] VAE Custom Shift/Scale
  - [x] CFM Lambda
  - [x] Keep Tokens/Tags Separator now correctly won't pass on it's value, if populated, downstream/when saving toml
  - [ ] Fix all 4 Subset Args' Optional Args checkbox groups

- [ ] Fix getting values from hardcoded dict and use actual UI default values correctly
  - [x] General Args/GeneralUI (Resolution, seed, etc)
  - [ ] ... find it in the other files ...
