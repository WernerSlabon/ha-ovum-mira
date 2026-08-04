# Home Assistant Integration for Ovum Mira Heatpump

<!--
> [!NOTE]  
> Highlights information that users should take into account, even when skimming.

> [!TIP]
> Optional information to help a user be more successful.

> [!IMPORTANT]  
> Crucial information necessary for users to succeed.

> [!WARNING]  
> Critical content demanding immediate user attention due to potential risks.

> [!CAUTION]
> Negative potential consequences of an action.
-->

This Home Assistant Integration is providing information from Ovum heat pumps with a Mira control unit.

__Please note__, _that this integration is not official and not supported by the Ovum development team. I am not affiliated with Ovum in any way._

> [!WARNING]
> ## General Disclaimer
> Please be aware that we are developing this integration to the best of our knowledge and belief, but can't give a guarantee. Therefore, use this integration **at your own risk**.

[![hacs_badge][hacsbadge]][hacs] [![hainstall][hainstallbadge]][hainstall] [![PayPal][paypalbadge]][paypal] [![github][ghsbadge]][ghs]

## Setup / Installation

### Step I: Install the integration

#### Option 1: via HACS

- Install [Home Assistant Community Store (HACS)](https://hacs.xyz/)
- Add the integration repository (search for "Ovum Mira" in "Explore & Download Repositories")
- Use the 3-dots at the right of the list entry (not at the top bar!) to download/install the custom integration — the latest release version is automatically selected. Only select a different version if you have specific reasons.
- After you press download and the process has completed, you must __Restart Home Assistant__ to install all dependencies
- Setup the custom integration as described below (see _Step II: Adding or enabling the integration_)

#### Option 2: manual steps

- Copy all files from `custom_components/ovum_mira/` to `custom_components/ovum_mira/` inside your config Home Assistant directory.
- Restart Home Assistant to install all dependencies
 
### Step II: Adding or enabling the integration

__You must have installed the integration (manually or via HACS before)!__

#### Option 1: My Home Assistant (2026.7+)

Just click the following Button to start the configuration automatically (for the rest see _Option 2: Manually steps by step_):

[![Open your Home Assistant instance and start setting up a new integration.](https://my.home-assistant.io/badges/config_flow_start.svg)](https://my.home-assistant.io/redirect/config_flow_start/?domain=ovum_mira)

#### Option 2: Manually step by step

Use the following steps for a manual configuration by adding the custom integration using the web interface and follow instruction on screen:

- Go to `Configuration -> Integrations` and add "Ovum Mira" integration
- Enter the IP-address or hostname of your Ovum Mira control unit
- Enter the ModbusTCP port the Mira control unit is listening (default: 502)
- Enter the PIN to authenticate the connection.  

You can repeat this to add other Ovum Mira heat pumps.

## Want to report an issue?

Please use the [GitHub Issues](https://github.com/WernerSlabon/ha-ovum-mira/issues) for reporting any issues you encounter with this integration. Please be so kind before creating a new issues, check the closed ones, if your problem have been already reported (& solved).