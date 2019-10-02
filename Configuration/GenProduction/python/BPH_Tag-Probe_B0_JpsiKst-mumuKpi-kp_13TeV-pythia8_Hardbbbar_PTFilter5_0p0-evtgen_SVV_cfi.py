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
# New definitions for psiKstar modes (Lange, July 26, 2000)
Define PKHplus  0.159
Define PKHzero  0.775
Define PKHminus 0.612
Define PKphHplus  1.563
Define PKphHzero  0.0
Define PKphHminus 2.712
#
#
Alias      MyK*0   K*0
#
Decay MyK*0
1.000      K+  pi-                VSS;
Enddecay
#
#
#
Alias     MyJ/psi    J/psi
Decay MyJ/psi
1.000      mu+  mu-              PHOTOS   VLL;
Enddecay
#
Decay B0
1.000     MyJ/psi  MyK*0         SVV_HELAMP PKHminus PKphHminus PKHzero PKphHzero PKHplus PKphHplus; #[Reconstructed PDG2011]
Enddecay
#
#
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
                    					# 'PTFilter:filter = on',
                                        # 'PTFilter:quarkToFilter = 5',
                                        # 'PTFilter:scaleToFilter = 1.0',
                                        # 'PTFilter:quarkPt = 0.0'
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
    DaughterIDs        = cms.untracked.vint32(443, 313),
    MinPt              = cms.untracked.vdouble(-1., -1),
    MinEta             = cms.untracked.vdouble(-9999999., -99999999.),
    MaxEta             = cms.untracked.vdouble( 9999999., 9999999.)
)

KstFilter = cms.EDFilter(
    "PythiaDauVFilter",
    ParticleID         = cms.untracked.int32(313),  ## K*0
    ChargeConjugation  = cms.untracked.bool(False),
    NumberDaughters    = cms.untracked.int32(2),
    DaughterIDs        = cms.untracked.vint32(-211, 321),
    MinPt              = cms.untracked.vdouble(0.5, 0.5),
    MinEta             = cms.untracked.vdouble(-3.0, -3.0),
    MaxEta             = cms.untracked.vdouble( 3.0, 3.0)
)

JpsiFilter = cms.EDFilter(
    "PythiaDauVFilter",
    ParticleID         = cms.untracked.int32(443),  ## K*0
    NumberDaughters    = cms.untracked.int32(2),
    DaughterIDs        = cms.untracked.vint32(-13, 13),
    MinPt              = cms.untracked.vdouble(1., 1.),
    MinEta             = cms.untracked.vdouble(-3.0, -3.0),
    MaxEta             = cms.untracked.vdouble( 3.0, 3.0)
)


ProductionFilterSequence = cms.Sequence(generator + mufilter + Bfilter + KstFilter + JpsiFilter)
