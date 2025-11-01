# InstaDMG

<div align="center">

![Platform](https://img.shields.io/badge/platform-macOS-lightgrey.svg)
![Version](https://img.shields.io/badge/version-1.6rc1-blue.svg)
![License](https://img.shields.io/badge/license-BSD-green.svg)
![Status](https://img.shields.io/badge/status-stable-success.svg)

**Create never-booted, modular macOS deployment images**

InstaDMG mirror from Google SVN

[Quick Start](#super-ultra-quickstart) • [Documentation](#step-by-step-build-guide) • [Advanced Topics](#advanced-topics) • [FAQ](#faq)

</div>

---

## 📋 Table of Contents

- [System Requirements](#system-requirements)
- [Super-Ultra-Quickstart](#super-ultra-quickstart)
- [Introduction](#introduction)
- [Step-by-Step Build Guide](#step-by-step-build-guide)
- [Understanding InstaUp2Date](#understanding-instaup2date)
- [Advanced Topics](#advanced-topics)
- [Performance Optimization](#performance-optimization)
- [FAQ](#faq)
- [Troubleshooting](#troubleshooting-1)
- [Related Resources](#related-resources)
- [Credits](#credits)

---

## System Requirements

### Hardware Requirements
- **Minimum RAM**: 2GB (4GB+ recommended)
- **Disk Space**: 20GB+ free space for builds
- **Storage**: SSD recommended for faster builds
- **Optional**: RAID0 array for optimal performance

### Software Requirements
- **macOS**: 10.5 (Leopard) or later for building
- **Python**: 2.7 (included in older macOS versions)
- **Git**: For cloning the repository
- **Admin Access**: Required for installation

### Supported Target OS Versions
- Mac OS X 10.5 (Leopard)
- Mac OS X 10.6 (Snow Leopard)
- Mac OS X 10.7 (Lion)
- Mac OS X 10.8 (Mountain Lion)

> **💡 Note:** While InstaDMG can run on newer macOS versions, it's designed for creating images of older OS X versions.

[🔝 Back to top](#instadmg)

---

## Super-Ultra-Quickstart

<details>
<summary><b>Click to expand quickstart instructions (Snow Leopard Version)</b></summary>

### Prerequisites
- OS X 10.6 (or 10.6.3) retail installer disk
- Admin access to your Mac

### Steps

1. **Clone the repository**
   
   Open Terminal and paste:
   
   ```bash
   git clone https://github.com/startergo/InstaDMG.git instadmg
   ```

2. **Import the installer disk**
   
   Insert your retail-box OS 10.6 installer disk, then run:
   
   ```bash
   sudo ./instadmg/AddOns/InstaUp2Date/importDisk.py --automatic --legacy
   ```
   
   ⏱️ This will take about 45 minutes.

3. **Process and build**
   
   ```bash
   sudo ./instadmg/AddOns/InstaUp2Date/instaUp2Date.py 10.6_vanilla --process
   ```
   
   ⏱️ This will take over an hour.

4. **Collect your image**
   
   Find your fully patched `10.6.8 Vanilla.dmg` in `./instadmg/OutputFiles/`.

Of course, there's much more to it than that!

> **💡 Pro Tip:** For your first run, use the default catalog files provided. You can customize later once you understand the workflow.

</details>

[🔝 Back to top](#instadmg)

---

## Introduction

<details>
<summary><b>Where InstaDMG Fits and What It Does</b></summary>

When setting up many new computers at once or refreshing existing workstations, it is of the utmost importance to have a known baseline you can count on. Out of the desire to 'slipstream' (loosely speaking) updates, software, and/or other enhancements into a baseline image that is hardware independent, `InstaDMG` was born. 

### Key Features

- **Never-Booted Images**: Creates images that can be customized through the addition of installer packages with the defining feature that the resulting image has never been booted
- **Modular Approach**: Enables a modular approach through installer packages
- **Best Practices**: Part of the "Preparation" step according to Apple's Best Practices for Client Management

### How It Works

Once we understand this specific use, it should be appreciated as part of the "Preparation" step according to Apple's Best Practices for Client Management (pdf). Being only the part that creates an image, it is easy to downplay its role if we don't appreciate the many deployment tools that can push out the resulting image in an optimized manner. 

`asr` is a binary that powers many of those tools, which is used to create and deploy images at the block-level (instead of file-level), which results in very fast restores.

Having become accustomed to the basic, straightforward way of manually configuring a workstation, we will need to take a different approach to get the changes we want to be applied to our image. Many of the common questions of how to effectively apply those customizations, that would otherwise have to be handled during the Maintenance and Control/Monitoring steps, have been solved by the community on the `afp548.com` forums.

### Workflow Overview

```
┌─────────────────┐
│  Clone Repo     │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Import Base OS │ (45 mins)
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Download Updates│ (via InstaUp2Date)
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Build Image    │ (60+ mins)
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Deploy via ASR  │ (3-5 mins)
└─────────────────┘
```

</details>

[🔝 Back to top](#instadmg)

---

## Step-by-Step Build Guide

### Step 1: Clone the Repository

```bash
git clone https://github.com/startergo/InstaDMG.git instadmg
```

This uses git to pull down the most recent version of the InstaDMG project into a newly-created folder called `instadmg` - it finishes in a matter of seconds, producing many lines of output and creating a very specific directory structure in your home folder.

### Step 2: Import the Installer Disk

```bash
sudo ./instadmg/AddOns/InstaUp2Date/importDisk.py --automatic --legacy
```

After prompting you for your (currently-logged-in admin) password, this prepares the inserted installer disk (DVD) by creating a dmg of it and placing that in the `./instadmg/InstallerFiles/BaseOS` folder. The `--automatic` option makes it skip prompting you for which disk you'd like to import, since we're assuming there is only one installer disk mounted, and places it in a `legacy` location. Expect this step to take around 45 minutes or so.

<details>
<summary><b>📝 Note for Lion (10.7) and Later</b></summary>

The above step isn't necessary or applicable since `10.7`, since `Lion` installer media is nested inside of `Install Mac OS X Lion.app` which can be downloaded from the Mac App Store. It is called `InstallESD.dmg`, and can be found by:

1. Right-clicking on the app
2. Choosing "Show Package Contents"
3. Navigating to `Contents/SharedSupport` folder

</details>

### Step 3: Process the Catalog

```bash
sudo ./instadmg/AddOns/InstaUp2Date/instaUp2Date.py 10.6_vanilla --process
```

The important thing to notice is the `--process` option, which triggers the transition from the `instaUp2Date` functionality (which pulls down the updates specified in the `10.6_vanilla.catalog` file) to the running of our key player, the `instadmg` bash script. The end result (after over an hour, surely enough time to grab a beverage) will be a ready-to-restore dmg in the `./instadmg/OutputFiles` folder.

> **✅ Success Indicator:** Look for a `.dmg` file in `OutputFiles/` with a name based on the current date or your custom name.

[🔝 Back to top](#instadmg)

---

## Understanding InstaUp2Date

<details>
<summary><b>What is InstaUp2Date?</b></summary>

It's a cause of confusion that `InstaUp2Date` is a project developed in parallel with `InstaDMG`, so we'll cover its benefits and use. Among other reasons, the wish to collaborate on a list of Apple patches to include in any generic image inspired the creation of `InstaUp2Date`. 

Sysadmins appreciate the utility of feeding a configuration file into the process (rather than merely passing a lot of flags and then parsing a log on the other end), and it acts as a documentation source to account for what went into an image.

### How It Works

In our quickstart earlier, the `InstaUp2Date` Python program takes its instructions from the `10.6_vanilla` catalog file, and then proceeds to download the updates listed and place them in a cache folder. Checking that you received the updates you wanted "as advertised" (i.e. not corrupted or altered) is done by verifying the SHA1 checksum, included in the catalog file.

Symbolic links (a.k.a. aliases or shortcuts, loosely speaking) are created to point from where `InstaDMG` would expect packages in the directory structure to where the files that have been cached. `InstaDMG` is then started up, via being called by the `--process` flag, at which point `instaup2date.py`'s most visible function is complete.

**For more information:** Check out `./instadmg/AddOns/InstaUp2Date/CatalogFiles/sample.catalog` and more comprehensive instructions can be found in the readme.

### Catalog File Structure

A typical catalog file contains:
- **Package URLs**: Direct links to Apple's software update servers
- **SHA1 Checksums**: For verifying package integrity
- **Installation Order**: Ensures proper update sequencing

**Example catalog entry:**
```
ARDClient3.5.4 sha1-5c22ffdabe875da62644331e63e64d6b27ad9afc.dmg	http://support.apple.com/downloads/DL1389/en_US/ARDClient3.5.4.dmg
```

</details>

[🔝 Back to top](#instadmg)

---

## Advanced Topics

<details>
<summary><b>Manual Package Management</b></summary>

If we're not utilizing `InstaUp2Date` to take care of the moving around of packages, we need to sort them ourselves. Adding packages (or mpkgs) to our image after the OS is installed, and making sure `iLife` gets installed before its updates are applied, means we need to get a handle on what order things are installed in. 

Even though many of these packages will be updates we get from Apple, it's a good idea to separate out the ones that deal with the core functionality of the OS (in `./instadmg/InstallerFiles/BaseUpdates`) and others, including software or peripheral-specific ones (which belong in `./instadmg/InstallerFiles/CustomPKG`).

### Determining Update Order

Manually running updates for the OS (or other products like `iLife` or `Microsoft Office`) with their native update software can make it easy to see exactly what order updates should be applied in. In the GUI you can check by going into System Preferences → Software Update and looking under the Installed Updates tab. Once we've assembled the update packages, we place them in numbered folders (01, 02, etc.) with one package per folder to be specific about their ordering.

</details>

<details>
<summary><b>BaseOS and InstallerChoices</b></summary>

The first fundamental part of all of this is the Operating System itself, referred to as the `BaseOS`. You are absolutely going to want to specify your own 'answer' file, which essentially checks boxes for you as if you were using the GUI installer process and making selections in the "customize" interface yourself. 

Examples are included for `Leopard` in the `./instadmg/Documentation/InstallerChoices` folder. Put the `InstallerChoices.xml` file in the folder with the OS (`./instadmg/InstallerFiles/BaseOS`) and `InstaDMG` will evaluate what to install based upon its contents.

### Why and How InstallerChoices Works

When you're de-selecting boxes in the GUI interface, it tells the installer to modify what to include in comparison to its Standard Install (which would be everything presented by default according to how Apple built the `mpkg`). Taking a step back, this customization is only possible when working with a `mpkg`. Since we can bundle many `pkg` installs into one `mpkg`, when the `mpkg` is built you may be able to specify certain things to leave out or include, whether or not they are even visible in the GUI installer.

### Creating Your Own InstallerChoices

The `InstallerChoices` readme has a link to a more thorough process, but a one-liner to get started with is:

```bash
sudo installer -showChoicesXML -pkg $PATH_TO_MPKG
```

Where `$PATH_TO_MPKG` would be `/Volumes/Mac\ OS\ X\ Install\ DVD/System/Installation/Packages/OSInstall.mpkg` in the case of the retail OS install itself.

### Using with Other Software

The particularly useful thing about learning how to take advantage of an answer file is that you can use the same process for other `mpkg`s, like `Office2008` and `iLife 09`, and then add the `xml` to the folder with the installer (this is all site licensed software we're working with, of course). Use the installer GUI as your guide, and give yourself a little background by looking at the full choicesXML for context, just in case the naming of the choices aren't clear.

</details>

<details>
<summary><b>Benefits and Caching</b></summary>

In an effort to make builds happen faster on subsequent runs, the base image (after `installerChoices` are evaluated) gets cached in `./instadmg/Caches/BaseOS`. `InstaDMG` will then look there from that point on, and subsequent runs skip that initial install step "for free".

</details>

<details>
<summary><b>Deploying Your Image</b></summary>

If you haven't already, you should look into `DeployStudio`, `PSU Blast Image Config`, or even just `asr` at the command line to restore your image. The usual warnings apply: this will wipe a disk clean before laying down your image - although all these tools are free, caveat emptor. You'll notice the restore process can be as fast as 3 minutes for a lean (< 6GB) image. 

Here's a one-liner for `asr` to get you going:

```bash
sudo asr restore --source /instadmg/OutputFiles/YYYY-MM-DD.dmg --target /Volumes/<Destination> --erase --verbose --noprompt --noverify --buffers 1 --buffersize 32m --puppetstrings
```

**⚠️ Warning:** Replace `YYYY-MM-DD` with your actual image name and `<Destination>` with your target volume name.

</details>

<details>
<summary><b>CreateUser Package</b></summary>

Included in the `AddOns` directory is a `createUser` package, which enables you to place a fresh, never logged in user account on the image. Almost everything you'd specify in System Preferences → Accounts when creating a new user can be customized here, and a tool to use which can generate an obscured password. 

This goes hand-in-hand with a very spare package that can be obtained from `afp548.com`'s `MyDownloads` section, called `clearReg`. This tricks the setup assistant to believe it has already run, along with the prompt for registration.

</details>

<details>
<summary><b>Checksum Tool</b></summary>

Revisiting `InstaUp2Date`, we'll touch on another helper file, `checksum.py`. This allows us to refer to custom `pkgs` we'd like to add in catalog files in the correct format (its output should be formatted with tabs exactly as required). Every time the 'fingerprint' or makeup of your package changes you will need to re-run this against your pkg and then update your catalog file accordingly. 

This is achieved with the following:

```bash
/instadmg/AddOns/InstaUp2Date/checksum.py $PATH_TO_PKG
```

(Where `$PATH_TO_PKG` usually lives in `/instadmg/InstallerFiles/InstaUp2DatePackages`)

</details>

<details>
<summary><b>Troubleshooting: Problems with Certain Installers</b></summary>

If getting your software to play well with `InstaDMG` (or deployment in general) isn't working for you, there are packaging tools that can 'capture' (like a snapshot) the state of a machine before and after install so you can repackage the differences. There are varying levels of success and complexity with the tools out there so we won't cover this topic in more depth, but a general recommendation is to run the software once before considering the capture stage complete.

### Recommended Packaging Tools
- **Composer** (by JAMF)
- **Packages** (by Stéphane Sudre)
- **AutoPkg** (for automated package creation)

</details>

[🔝 Back to top](#instadmg)

---

## Performance Optimization

<details>
<summary><b>Click to expand optimization tips</b></summary>

Once we've got the workflow down, it's all about optimization. Disk image creation is a heavy I/O process, so CPU and RAM don't play as much of a factor (although only having 1GB RAM is painful in general). There is one step in the process that can be skipped, and other helpful flags demonstrated below:

```bash
sudo ./instadmg/instadmg.bash -f -t /Volumes/stripedRAID0 -o /Volumes/stripedRAID0 -m Dev_10-6-5 -n Restored
```

### Command Line Flags

| Flag | Description |
|------|-------------|
| `-f` | **Non-paranoid mode** - Skips verification of image checksums |
| `-t` | **Temp location** - Specifies location for writing the intermediate image (instead of default `/tmp`) |
| `-o` | **Output location** - Specifies output location for final ASR-ready image (instead of `./instadmg/OutputFiles/`) |
| `-m` | **Image name** - Sets the name for the resulting ASR image before restoration (e.g., `Dev_10-6-5.dmg` instead of date-based naming) |
| `-n` | **Partition name** - Sets the partition name after restoration (e.g., `Restored` instead of default `InstaDMG`) |

### Performance Tips

The subsequent flags have the effect of multiplying the 'spindles' doing the work:

- **InstaDMG directory** can be housed on a separate disk for the sole purpose of reading the packages (these days that would be an SSD with its superior sequential reads nearly saturating the SATA bus)
- **Another location** designated by the `-t` flag (in this example a RAID0 volume) is utilized for both writing the intermediate image into its root directory and putting the final ASR-ready output

### Getting Help

These are scripts you can open and look at, so feel free to read through all the options, or pass the `--help` flag to it. And please post on the forum at `afp548.com` with questions!

### Real-World Performance Example

**Typical build times:**
- Standard HDD: ~2-3 hours
- SSD: ~1-1.5 hours  
- SSD + RAID0 (optimized): ~45-60 minutes

</details>

[🔝 Back to top](#instadmg)

---

## FAQ

<details>
<summary><b>How do I update to the latest version?</b></summary>

Navigate to your InstaDMG directory and run:

```bash
cd instadmg
git pull origin main
```

</details>

<details>
<summary><b>Can I create images for multiple OS versions?</b></summary>

Yes! InstaDMG supports multiple OS versions. Simply import different installer discs and use the appropriate catalog files (e.g., `10.6_vanilla.catalog`, `10.7_vanilla.catalog`).

</details>

<details>
<summary><b>Why is my build taking longer than expected?</b></summary>

Several factors affect build time:
- **Disk speed**: HDDs are significantly slower than SSDs
- **Network speed**: Downloading updates depends on your connection
- **System resources**: Available RAM and CPU affect performance
- **Cache state**: First builds take longer; subsequent builds use cached base images

</details>

<details>
<summary><b>Can I add third-party software to my image?</b></summary>

Yes! Place installer packages in:
- `./instadmg/InstallerFiles/CustomPKG/` for additional software
- Use numbered folders (01, 02, 03, etc.) to control installation order

</details>

<details>
<summary><b>What's the difference between InstaDMG and other imaging solutions?</b></summary>

InstaDMG creates **never-booted** images, meaning:
- No unique identifiers are generated
- No system-specific configurations exist
- Images are hardware-independent
- Perfect for mass deployment

Other solutions often create images from a booted system, which can cause issues when deployed to multiple machines.

</details>

<details>
<summary><b>Do I need an internet connection?</b></summary>

Yes, for the initial download of updates via InstaUp2Date. However, once updates are cached, you can build offline by reusing cached packages.

</details>

<details>
<summary><b>How do I customize which OS components are installed?</b></summary>

Create an `InstallerChoices.xml` file and place it in `./instadmg/InstallerFiles/BaseOS/`. See the [BaseOS and InstallerChoices](#advanced-topics) section for details.

</details>

<details>
<summary><b>Can I run InstaDMG on Apple Silicon (M1/M2) Macs?</b></summary>

InstaDMG was designed for Intel Macs and older OS X versions. Running on Apple Silicon may require Rosetta 2, and functionality is not guaranteed for creating images of very old OS versions.

</details>

[🔝 Back to top](#instadmg)

---

## Troubleshooting

<details>
<summary><b>Common Issues and Solutions</b></summary>

### Issue: Permission Denied Errors

**Solution:** Ensure you're running commands with `sudo` where required:
```bash
sudo ./instadmg/AddOns/InstaUp2Date/importDisk.py --automatic --legacy
```

### Issue: Disk Import Fails

**Symptoms:** Error during `importDisk.py` execution

**Solutions:**
1. Verify you have a genuine retail installer disc (not an upgrade disc)
2. Check disk is mounted: `ls /Volumes/`
3. Ensure sufficient disk space (20GB+ free)
4. Try manual import without `--automatic` flag

### Issue: Checksum Verification Fails

**Symptoms:** SHA1 mismatch errors

**Solutions:**
1. Delete corrupted downloads from cache: `rm -rf ./instadmg/Caches/InstaUp2DateCache/*`
2. Re-run the build process
3. Check your internet connection stability

### Issue: Build Process Hangs

**Solutions:**
1. Check `/var/log/system.log` for errors
2. Verify available disk space: `df -h`
3. Monitor activity: `tail -f ./instadmg/Logs/*.log`
4. Kill and restart the process if necessary

### Issue: Python Script Won't Run

**Symptoms:** `python: command not found` or version errors

**Solutions:**
1. Verify Python installation: `python --version`
2. Install Python 2.7 if missing (required for older scripts)
3. Check script permissions: `chmod +x ./instadmg/AddOns/InstaUp2Date/*.py`

### Issue: Output Image Won't Boot

**Solutions:**
1. Verify image was created successfully (check file size)
2. Use Disk Utility to verify the DMG
3. Ensure you're using `asr` for restoration, not simple copy
4. Check that target hardware is supported by the OS version

### Getting More Help

- **Check Logs:** `./instadmg/Logs/` contains detailed build logs
- **Verbose Mode:** Run with `-v` flag for detailed output
- **Community Forums:** Post on `afp548.com` with log excerpts
- **GitHub Issues:** Report bugs on the repository

</details>

[🔝 Back to top](#instadmg)

---

## Related Resources

### Documentation
- 📖 [Apple Software Update Catalogs](https://support.apple.com/en-us/HT201222)
- 📖 [ASR Command Reference](https://ss64.com/osx/asr.html)
- 📖 [Installer Choices Reference](https://www.afp548.com)

### Tools & Software
- 🛠️ [DeployStudio](http://www.deploystudio.com/) - Free imaging and deployment solution
- 🛠️ [AutoDMG](https://github.com/MagerValp/AutoDMG) - Modern alternative for newer OS versions
- 🛠️ [Packages](http://s.sudre.free.fr/Software/Packages/about.html) - Package creator
- 🛠️ [Composer](https://www.jamf.com/products/jamf-composer/) - Professional package creation tool

### Community
- 💬 [AFP548 Forums](https://www.afp548.com) - Mac admin community
- 💬 [MacAdmins Slack](https://macadmins.org/) - Active community chat
- 💬 [r/macsysadmin](https://www.reddit.com/r/macsysadmin/) - Reddit community

### Related Projects
- 🔗 [AutoPkg](https://github.com/autopkg/autopkg) - Automated package management
- 🔗 [munki](https://github.com/munki/munki) - Managed software installation
- 🔗 [Imagr](https://github.com/grahamgilbert/imagr) - Deployment workflow tool

[🔝 Back to top](#instadmg)

---

## Credits

**Questions/feedback about this guide?** instadmg.docs@gmail.com

### Roll Credits and Thanks

To you, for reading this far, contributors past and future:

Mr. Kuehn, Mr. Wisenbaker, Mr. Fergus, Mr. Akins, Mr. Meyer, Mr. Larizza, Mr. Walck, Mr. van Bochoven, and many others...

---

## Contributing

Contributions are welcome! If you'd like to contribute:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## License

This project maintains its original BSD-style license. See the LICENSE file in the repository for details.

---

## Changelog

### Version 1.6rc1
- Stable release candidate
- Support for OS X 10.5-10.8
- InstaUp2Date integration
- Catalog-based update management

[🔝 Back to top](#instadmg)

---

<div align="center">

**⭐ If you find InstaDMG useful, please star this repository! ⭐**

*Creating never-booted macOS deployment images since the early days.*

Made with ❤️ by the Mac Admin community

</div>
