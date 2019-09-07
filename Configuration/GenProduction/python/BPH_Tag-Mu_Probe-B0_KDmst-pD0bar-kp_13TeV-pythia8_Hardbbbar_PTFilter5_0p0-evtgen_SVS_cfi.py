import FWCore.ParameterSet.Config as cms
from Configuration.Generator.Pythia8CommonSettings_cfi import *
from Configuration.Generator.MCTunes2017.PythiaCP5Settings_cfi import *

generator = cms.EDFilter("Pythia8GeneratorFilter",
    pythiaPylistVerbosity = cms.untracked.int32(0),
    pythiaHepMCVerbosity = cms.untracked.bool(False),
    maxEventsToPrint = cms.untracked.int32(0),
    comEnergy = cms.double(13000.0),
    ExternalDecays = cms.PSet(
        EvtGen130 = cms.untracked.PSet(
            decay_table = cms.string('GeneratorInterface/EvtGenInterface/data/DECAY_2014_NOLONGLIFE.DEC'),
            particle_property_file = cms.FileInPath('GeneratorInterface/EvtGenInterface/data/evt_2014.pdl'),
            convertPythiaCodes = cms.untracked.bool(False),
            user_decay_embedded= cms.vstring(
"""
Alias      MyD0   D0
Alias      Myanti-D0   anti-D0
ChargeConj MyD0   Myanti-D0
#
Decay MyD0
1.000      K-  pi+                PHSP;
Enddecay
CDecay Myanti-D0
#
#
#
Alias     MyD*-    D*-
Decay MyD*-
1.000      Myanti-D0 pi-          VSS;
Enddecay
#
Decay B0
1.000     MyD*- K+         PHOTOS  SVS;
Enddecay
#
#
######## Forcing the other B to always decay into a muon ##############
#
Decay anti-B0
1.000     D*+ mu- anti-nu_mu        PHOTOS ISGW2;
Enddecay
#
Decay B+
1.000     anti-D*0 mu+ nu_mu        PHOTOS ISGW2;
Enddecay
CDecay B-
#
Decay B_s0
1.000   D_s*-    mu+    nu_mu        PHOTOS  ISGW2;
Enddecay
CDecay anti-B_s0
End
"""
                                            )
        ),
        parameterSets = cms.vstring('EvtGen130')
    ),
    PythiaParameters = cms.PSet(
        pythia8CommonSettingsBlock,
        pythia8CP5SettingsBlock,
        processParameters = cms.vstring(
                                        'HardQCD:hardbbbar = on',
                    					'PTFilter:filter = on',
                                        'PTFilter:quarkToFilter = 5',
                                        'PTFilter:scaleToFilter = 1.0',
                                        'PTFilter:quarkPt = 0.0'
            ),
        parameterSets = cms.vstring('pythia8CommonSettings',
                                    'pythia8CP5Settings',
                                    'processParameters',
                                    )
    )
)


###### Filters ##########
mufilter = cms.EDFilter("PythiaFilter",
    MaxEta = cms.untracked.double(2.5),
    MinEta = cms.untracked.double(-2.5),
    MinPt = cms.untracked.double(6.5),
    ParticleID = cms.untracked.int32(13),
)

Bfilter = cms.EDFilter(
    "PythiaDauVFilter",
    ParticleID         = cms.untracked.int32(511),  ## B0
    ChargeConjugation  = cms.untracked.bool(False),
    NumberDaughters    = cms.untracked.int32(2),
    DaughterIDs        = cms.untracked.vint32(-413, 321),
    MinPt              = cms.untracked.vdouble(-1., 0.3),
    MinEta             = cms.untracked.vdouble(-9999999., -3.),
    MaxEta             = cms.untracked.vdouble( 9999999., 3.)
)


ProductionFilterSequence = cms.Sequence(generator + mufilter + Bfilter)
