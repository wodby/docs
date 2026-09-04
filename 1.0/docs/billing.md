# Billing and Payment

## Overview

Wodby subscriptions are priced per [application instance](apps/instances.md). You can find the available plans on [our pricing page](https://wodby.com/pricing-plans).

## Starting a paid subscription

New paid subscriptions start billing immediately and do not include a free trial. Existing trial subscriptions continue until their scheduled end.

To subscribe, open `Billing > Plan`, choose the Team plan, and confirm the change. Wodby redirects you to Stripe Checkout to collect your billing and payment details. Stripe asks for additional payment authentication, such as 3D Secure, when it is required. Your subscription is updated after Checkout succeeds.

## Payment methods

Payment details are collected and stored by [Stripe](https://stripe.com). Wodby does not receive or store the card number or security code. It keeps only the Stripe reference and limited display information, such as the card brand and last four digits.

Open `Billing > Card` to add or replace the organization's default card. Wodby redirects you to Stripe Billing Portal for the update and returns you to the dashboard when it is complete. To permanently remove a payment method without replacing it, [contact support](support.md).

## Billing

At the beginning of every billing month, you are charged for the number of instances in the organization, with a minimum of 10 instances, regardless of their status. Instance-count changes during the month are accounted for in the next billing period based on instance-hours.

Subscriptions renew automatically on the schedule shown in the dashboard, and Stripe charges the organization's default payment method.

If you cancel a subscription, it remains active until the end of the current billing period and is not renewed.

## Container registry storage

Wodby provides a private docker registry `registry.wodby.com` that stores the images built and released during your deployments. See [deployment](apps/deploy.md#release) for how images are pushed to it.

Every organization includes 5 GB of registry storage. Storage above the included amount is billed at $0.15 per GB per month.

Deleting images you no longer need reduces your stored amount. Images that belong to deleted applications and instances are cleaned up automatically.

## Invoices

After every successful charge, Wodby sends an invoice to the billing email specified under `Billing > Settings`, or to the billing contact associated with the Stripe customer. You can also find all invoices and download them as PDF files under `Billing > Invoices`.

## Billing address and VAT

You can specify the required billing details under `Billing > Settings`. The details appear on your invoices. Stripe Checkout also collects the billing address needed to process a new subscription.

## Permissions

All organization owners can manage the organization's payment method and subscription.

## Discount

Contact [support](support.md) to discuss annual or volume pricing.
