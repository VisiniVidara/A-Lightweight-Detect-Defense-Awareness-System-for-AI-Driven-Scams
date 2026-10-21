"use strict";
(()=>{
 const dialog=document.getElementById('purchase-demo'),form=document.getElementById('demo-checkout-form'),content=document.getElementById('demo-checkout-content'),success=document.getElementById('demo-purchase-success'),feedback=document.getElementById('demo-payment-feedback'),pay=document.getElementById('demo-pay');
 const el=id=>document.getElementById(id);
 function reset(){form.reset();el('demo-card').value='';el('demo-expiry').value='';el('demo-cvc').value='';feedback.textContent='';content.hidden=false;success.hidden=true;pay.disabled=false;}
 document.addEventListener('mailsentra:checkout',event=>{reset();el('demo-customer').value=event.detail.name;el('demo-email').value=event.detail.email;dialog.showModal();});
 el('close-purchase-demo').addEventListener('click',()=>dialog.close());
 dialog.addEventListener('close',reset);
 el('fill-demo-card').addEventListener('click',()=>{el('demo-card').value='4242 4242 4242 4242';el('demo-expiry').value='12/30';el('demo-cvc').value='123';feedback.textContent='Visa test details filled. Select the simulation acknowledgement to continue.';});
 el('demo-purchase-again').addEventListener('click',()=>{reset();dialog.scrollTop=0;el('demo-customer').focus();});
 form.addEventListener('submit',e=>{
 e.preventDefault();if(!form.reportValidity())return;
 const card=el('demo-card').value.replace(/\s/g,'');
 if(!['4242424242424242','5555555555554444'].includes(card)||el('demo-expiry').value!=='12/30'||el('demo-cvc').value!=='123'){feedback.textContent='Use only the supplied Visa or Mastercard test number, expiry 12/30 and security code 123. Real card details are not accepted.';el('demo-card').value='';el('demo-cvc').value='';return;}

 content.hidden=true;success.hidden=false;el('demo-reference').textContent='DEMO-'+crypto.randomUUID().slice(0,8).toUpperCase();el('demo-card').value='';el('demo-cvc').value='';el('demo-expiry').value='';success.focus();dialog.scrollTop=0;
 });
})();
